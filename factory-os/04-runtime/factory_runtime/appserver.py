from __future__ import annotations

import json
import os
import queue
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from .models import ModelCapability, QuotaSnapshot, RuntimeSnapshot


class ProbeError(RuntimeError):
    pass


class _JsonlRpcClient:
    def __init__(self, process: subprocess.Popen[str], timeout: float):
        self.process = process
        self.timeout = timeout
        self._next_id = 1
        self._lines: queue.Queue[dict[str, Any]] = queue.Queue()
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    def _read_loop(self) -> None:
        assert self.process.stdout is not None
        for line in self.process.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(msg, dict):
                self._lines.put(msg)

    def send(self, payload: dict[str, Any]) -> None:
        assert self.process.stdin is not None
        self.process.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        self.process.stdin.flush()

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        self.send(payload)

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        req_id = self._next_id
        self._next_id += 1
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            payload["params"] = params
        self.send(payload)
        deadline = time.monotonic() + self.timeout
        deferred: list[dict[str, Any]] = []
        try:
            while time.monotonic() < deadline:
                remaining = max(0.01, deadline - time.monotonic())
                try:
                    msg = self._lines.get(timeout=remaining)
                except queue.Empty:
                    break
                if msg.get("id") == req_id:
                    if "error" in msg:
                        raise ProbeError(f"app-server {method} error: {msg['error']}")
                    result = msg.get("result")
                    return result if isinstance(result, dict) else {"value": result}
                deferred.append(msg)
        finally:
            for msg in deferred:
                self._lines.put(msg)
        raise ProbeError(f"timeout waiting for app-server response to {method}")


class AppServerProbe:
    """Short-lived, fail-open probe for Codex model availability and quota state.

    Uses the documented newline-delimited JSON-RPC stdio transport. The probe is
    deliberately observational: it never starts a model turn, consumes reset
    credits, or changes account state.
    """

    def __init__(
        self,
        codex_bin: str = "codex",
        timeout: float = 3.0,
        env: dict[str, str] | None = None,
    ) -> None:
        self.codex_bin = codex_bin
        self.timeout = timeout
        self.env = env or {}

    def _resolve_binary(self) -> str:
        if os.path.isabs(self.codex_bin) and Path(self.codex_bin).exists():
            return self.codex_bin
        resolved = shutil.which(self.codex_bin)
        if not resolved:
            raise ProbeError(f"Codex binary not found: {self.codex_bin}")
        return resolved

    def _version(self, binary: str) -> str | None:
        try:
            cp = subprocess.run(
                [binary, "--version"], capture_output=True, text=True,
                timeout=min(self.timeout, 2.0), env={**os.environ, **self.env},
            )
        except Exception:
            return None
        text = (cp.stdout or cp.stderr or "").strip()
        match = re.search(r"(\d+\.\d+(?:\.\d+)?(?:[-+][\w.-]+)?)", text)
        return match.group(1) if match else (text or None)

    def probe(self, include_hidden: bool = False, include_quota: bool = True) -> RuntimeSnapshot:
        binary = self._resolve_binary()
        warnings: list[str] = []
        proc = subprocess.Popen(
            [binary, "app-server", "--listen", "stdio://"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env={**os.environ, **self.env},
        )
        client = _JsonlRpcClient(proc, self.timeout)
        try:
            client.request(
                "initialize",
                {
                    "clientInfo": {"name": "codex-factory-os-probe", "title": "Codex Factory OS Probe", "version": "1.1.0"},
                    "capabilities": {"experimentalApi": True},
                },
            )
            client.notify("initialized", {})
            model_result = client.request("model/list", {"limit": 100, "includeHidden": include_hidden})
            models = tuple(
                ModelCapability.from_appserver(item)
                for item in (model_result.get("data") or [])
                if isinstance(item, dict) and (item.get("id") or item.get("model"))
            )
            quota = None
            if include_quota:
                try:
                    quota_result = client.request("account/rateLimits/read", {"supportsLunaReserve": True})
                    quota = QuotaSnapshot.from_appserver(quota_result)
                except ProbeError as exc:
                    warnings.append(f"quota probe unavailable: {exc}")
            return RuntimeSnapshot(
                models=models,
                quota=quota,
                codex_version=self._version(binary),
                probe_ok=True,
                warnings=tuple(warnings),
            )
        finally:
            try:
                if proc.stdin:
                    proc.stdin.close()
            except Exception:
                pass
            try:
                proc.terminate()
                proc.wait(timeout=0.5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass

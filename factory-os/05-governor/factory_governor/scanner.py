from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback not bundled
    tomllib = None  # type: ignore[assignment]

from .models import Resource

FACTORY_MARKERS = (
    "codex factory os",
    "factory os control plane",
    "factory-governor",
    "factory_router",
    "factory-runtime",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _ownership(path: Path, content: str, repo_root: Path | None) -> str:
    low = (str(path) + "\n" + content[:12000]).lower()
    if any(marker in low for marker in FACTORY_MARKERS):
        return "factory_os"
    if repo_root is not None:
        try:
            path.resolve().relative_to(repo_root.resolve())
            return "project"
        except Exception:
            pass
    if any(part in {"node_modules", "vendor", ".venv", "site-packages"} for part in path.parts):
        return "third_party"
    return "unknown"


def _resource_id(kind: str, scope: str, path: Path, name: str) -> str:
    raw = f"{kind}|{scope}|{path}|{name}".encode("utf-8", errors="replace")
    return hashlib.sha1(raw).hexdigest()[:16]


def _resource(kind: str, name: str, path: Path, scope: str, repo_root: Path | None,
              enabled: bool | None = None, metadata: dict[str, Any] | None = None) -> Resource:
    content = _read_text(path) if path.is_file() else ""
    return Resource(
        id=_resource_id(kind, scope, path, name),
        kind=kind,  # type: ignore[arg-type]
        name=name,
        path=str(path),
        scope=scope,
        ownership=_ownership(path, content, repo_root),  # type: ignore[arg-type]
        enabled=enabled,
        sha256=sha256_file(path) if path.is_file() else None,
        metadata=metadata or {},
    )


def _load_toml(path: Path) -> dict[str, Any]:
    if tomllib is None or not path.exists():
        return {}
    try:
        with path.open("rb") as f:
            return tomllib.load(f)
    except Exception as exc:
        return {"__parse_error__": str(exc)}


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"\'')
    return out


def _scan_agents_guidance(base: Path, scope: str, repo_root: Path | None) -> list[Resource]:
    out: list[Resource] = []
    for name in ("AGENTS.override.md", "AGENTS.md"):
        path = base / name
        if path.is_file():
            out.append(_resource("agents_guidance", name, path, scope, repo_root,
                                 metadata={"override": name.endswith("override.md")}))
    return out


def _scan_skills(root: Path, scope: str, repo_root: Path | None) -> list[Resource]:
    if not root.exists():
        return []
    out: list[Resource] = []
    for skill_md in root.glob("*/SKILL.md"):
        text = _read_text(skill_md)
        fm = _frontmatter(text)
        name = fm.get("name") or skill_md.parent.name
        enabled = None
        out.append(_resource("skill", name, skill_md, scope, repo_root, enabled=enabled,
                             metadata={"description": fm.get("description", ""), "skill_dir": str(skill_md.parent)}))
    return out


def _scan_custom_agents(root: Path, scope: str, repo_root: Path | None) -> list[Resource]:
    if not root.exists():
        return []
    out: list[Resource] = []
    for path in sorted(root.glob("*.toml")):
        data = _load_toml(path)
        name = str(data.get("name") or path.stem)
        out.append(_resource(
            "custom_agent", name, path, scope, repo_root,
            metadata={
                "model": data.get("model"),
                "model_reasoning_effort": data.get("model_reasoning_effort"),
                "sandbox_mode": data.get("sandbox_mode"),
                "description": data.get("description", ""),
                "parse_error": data.get("__parse_error__"),
            },
        ))
    return out


def _scan_rules(root: Path, scope: str, repo_root: Path | None) -> list[Resource]:
    if not root.exists():
        return []
    out: list[Resource] = []
    for path in sorted(root.glob("*.rules")):
        text = _read_text(path)
        decisions = re.findall(r'decision\s*=\s*["\'](allow|prompt|forbidden)["\']', text)
        patterns = re.findall(r'pattern\s*=\s*\[(.*?)\]', text, flags=re.S)
        out.append(_resource("rule", path.name, path, scope, repo_root,
                             metadata={"decisions": decisions, "pattern_count": len(patterns)}))
    return out


def _scan_hooks(layer: Path, scope: str, repo_root: Path | None, config: dict[str, Any]) -> list[Resource]:
    out: list[Resource] = []
    path = layer / "hooks.json"
    if path.is_file():
        try:
            data = json.loads(_read_text(path))
            events = sorted((data.get("hooks") or {}).keys()) if isinstance(data, dict) else []
            parse_error = None
        except Exception as exc:
            events, parse_error = [], str(exc)
        out.append(_resource("hook", "hooks.json", path, scope, repo_root,
                             metadata={"format": "hooks.json", "events": events, "parse_error": parse_error}))
    if isinstance(config.get("hooks"), dict):
        cfg_path = layer / "config.toml"
        out.append(_resource("hook", "inline-hooks", cfg_path, scope, repo_root,
                             metadata={"format": "config.toml", "events": sorted(config["hooks"].keys())}))
    return out


def _scan_config(layer: Path, scope: str, repo_root: Path | None) -> tuple[list[Resource], dict[str, Any]]:
    path = layer / "config.toml"
    if not path.is_file():
        return [], {}
    data = _load_toml(path)
    resources = [_resource("config", "config.toml", path, scope, repo_root,
                           metadata={"parse_error": data.get("__parse_error__")})]
    mcps = data.get("mcp_servers") or {}
    if isinstance(mcps, dict):
        for name, cfg in sorted(mcps.items()):
            cfg = cfg if isinstance(cfg, dict) else {"value": cfg}
            resources.append(Resource(
                id=_resource_id("mcp", scope, path, str(name)),
                kind="mcp",
                name=str(name),
                path=str(path),
                scope=scope,
                ownership=_ownership(path, _read_text(path), repo_root),  # type: ignore[arg-type]
                enabled=cfg.get("enabled") if isinstance(cfg.get("enabled"), bool) else None,
                sha256=sha256_file(path),
                metadata={
                    "command": cfg.get("command"),
                    "url": cfg.get("url"),
                    "transport": cfg.get("transport"),
                    "startup_timeout_sec": cfg.get("startup_timeout_sec"),
                },
            ))
    return resources, data


def scan_environment(codex_home: Path, repo_root: Path | None = None, user_home: Path | None = None) -> list[Resource]:
    codex_home = codex_home.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve() if repo_root else None
    user_home = (user_home or codex_home.parent).expanduser().resolve()
    resources: list[Resource] = []

    # Global Codex layer
    resources.extend(_scan_agents_guidance(codex_home, "global", repo_root))
    cfg_resources, global_cfg = _scan_config(codex_home, "global", repo_root)
    resources.extend(cfg_resources)
    resources.extend(_scan_hooks(codex_home, "global", repo_root, global_cfg))
    resources.extend(_scan_custom_agents(codex_home / "agents", "global", repo_root))
    resources.extend(_scan_rules(codex_home / "rules", "global", repo_root))
    resources.extend(_scan_skills(user_home / ".agents" / "skills", "global", repo_root))

    # Project-local Codex layer and guidance.
    if repo_root:
        resources.extend(_scan_agents_guidance(repo_root, "project", repo_root))
        project_codex = repo_root / ".codex"
        cfg_resources, project_cfg = _scan_config(project_codex, "project", repo_root)
        resources.extend(cfg_resources)
        resources.extend(_scan_hooks(project_codex, "project", repo_root, project_cfg))
        resources.extend(_scan_custom_agents(project_codex / "agents", "project", repo_root))
        resources.extend(_scan_rules(project_codex / "rules", "project", repo_root))
        resources.extend(_scan_skills(repo_root / ".agents" / "skills", "project", repo_root))

        # Nested AGENTS files matter to Codex. Keep bounded and skip common generated dirs.
        skip = {".git", ".venv", "venv", "node_modules", "dist", "build", "vendor"}
        for root, dirs, files in os.walk(repo_root):
            dirs[:] = [d for d in dirs if d not in skip]
            root_path = Path(root)
            if root_path == repo_root:
                continue
            for name in ("AGENTS.override.md", "AGENTS.md"):
                if name in files:
                    path = root_path / name
                    resources.append(_resource("agents_guidance", name, path, "project-nested", repo_root,
                                               metadata={"override": name.endswith("override.md")}))

    return resources

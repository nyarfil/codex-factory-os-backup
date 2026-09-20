from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from .fsutil import atomic_write_json

FACTORY_TOKEN = "factory-os-managed"


def load_hooks(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"hooks": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("hooks.json root must be an object")
    data.setdefault("hooks", {})
    if not isinstance(data["hooks"], dict):
        raise ValueError("hooks.json 'hooks' must be an object")
    return data


def _cmd(script: Path) -> str:
    # Codex command hooks accept a shell command string. Quote both executable and script path.
    exe = str(Path(sys.executable).resolve())
    return f'"{exe}" "{script.resolve()}"'


def factory_hook_groups(install_root: Path) -> dict[str, list[dict[str, Any]]]:
    hooks_dir = install_root / "04-runtime" / "hooks"
    specs = {
        "SessionStart": ("startup|resume|clear|compact", "session_start.py", 5, 1024),
        "UserPromptSubmit": (None, "user_prompt_submit.py", 5, 1024),
        "PreToolUse": ("Agent|spawn_agent", "pre_tool_use_agent.py", 3, 1024),
        "SubagentStart": (".*", "subagent_start.py", 3, 1024),
        "SubagentStop": (".*", "subagent_stop.py", 3, None),
    }
    out: dict[str, list[dict[str, Any]]] = {}
    for event, (matcher, filename, timeout, ctx_limit) in specs.items():
        handler: dict[str, Any] = {
            "type": "command",
            "command": _cmd(hooks_dir / filename),
            "timeout": timeout,
            "statusMessage": f"{FACTORY_TOKEN}:{event}",
        }
        if ctx_limit is not None:
            handler["additionalContextLimit"] = ctx_limit
        group: dict[str, Any] = {"hooks": [handler]}
        if matcher:
            group["matcher"] = matcher
        out[event] = [group]
    return out


def _is_factory_group(group: Any) -> bool:
    if not isinstance(group, dict):
        return False
    for handler in group.get("hooks", []):
        if not isinstance(handler, dict):
            continue
        if FACTORY_TOKEN in str(handler.get("statusMessage", "")):
            return True
        if "factory-os" in str(handler.get("command", "")).lower() and "04-runtime" in str(handler.get("command", "")).lower():
            return True
    return False


def merge_factory_hooks(path: Path, install_root: Path) -> tuple[bool, int]:
    data = load_hooks(path)
    hooks = copy.deepcopy(data.get("hooks", {}))
    desired = factory_hook_groups(install_root)
    removed = 0
    for event, groups in list(hooks.items()):
        if not isinstance(groups, list):
            continue
        clean = [g for g in groups if not _is_factory_group(g)]
        removed += len(groups) - len(clean)
        hooks[event] = clean
    for event, groups in desired.items():
        hooks.setdefault(event, [])
        hooks[event].extend(groups)
    data["hooks"] = hooks
    before = path.read_text(encoding="utf-8") if path.exists() else None
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    changed = rendered != before
    if changed:
        atomic_write_json(path, data)
    return changed, removed


def remove_factory_hooks(path: Path) -> tuple[bool, int]:
    if not path.exists():
        return False, 0
    data = load_hooks(path)
    hooks = data.get("hooks", {})
    removed = 0
    for event in list(hooks):
        groups = hooks.get(event)
        if not isinstance(groups, list):
            continue
        clean = [g for g in groups if not _is_factory_group(g)]
        removed += len(groups) - len(clean)
        if clean:
            hooks[event] = clean
        else:
            hooks.pop(event, None)
    data["hooks"] = hooks
    if removed == 0:
        return False, 0
    # If only our top-level description remains and no hooks, delete. Otherwise preserve file.
    if not hooks and set(data).issubset({"hooks", "description"}):
        path.unlink()
    else:
        atomic_write_json(path, data)
    return True, removed

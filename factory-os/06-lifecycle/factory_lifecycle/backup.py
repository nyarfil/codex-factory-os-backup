from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .fsutil import atomic_write_json, sha256_file


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def create_backup(codex_home: Path, user_home: Path, backup_base: Path | None = None) -> Path:
    backup_base = backup_base or (codex_home / "factory-os-backups")
    target = backup_base / _stamp()
    n = 1
    while target.exists():
        target = backup_base / f"{_stamp()}-{n}"
        n += 1
    target.mkdir(parents=True, exist_ok=False)

    manifest: list[dict[str, str]] = []
    candidates = [
        codex_home / "AGENTS.md",
        codex_home / "AGENTS.override.md",
        codex_home / "config.toml",
        codex_home / "hooks.json",
    ]
    dirs = [codex_home / "agents", codex_home / "rules", user_home / ".agents" / "skills"]

    for src in candidates:
        if src.is_file():
            rel = Path("codex") / src.name
            dst = target / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            manifest.append({"source": str(src), "backup": str(rel), "sha256": sha256_file(src)})
    for src_dir in dirs:
        if not src_dir.is_dir():
            continue
        label = "skills" if src_dir.name == "skills" else src_dir.name
        dst_root = target / label
        shutil.copytree(src_dir, dst_root)
        for src in src_dir.rglob("*"):
            if src.is_file():
                rel = Path(label) / src.relative_to(src_dir)
                manifest.append({"source": str(src), "backup": str(rel), "sha256": sha256_file(src)})

    atomic_write_json(target / "backup-manifest.json", {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "codex_home": str(codex_home),
        "user_home": str(user_home),
        "files": manifest,
    })
    return target

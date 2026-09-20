from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .backup import create_backup
from .models import LifecycleReport

ALLOWED_OPS={"quarantine_path", "restore_path"}


def load_plan(path: Path) -> dict[str, Any]:
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("operations"), list):
        raise ValueError("cleanup plan must be an object with an operations array")
    return data


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve()); return True
    except Exception:
        return False


def execute_cleanup(plan_path: Path, codex_home: Path, user_home: Path, *, apply: bool = False,
                    backup_base: Path | None = None) -> LifecycleReport:
    codex_home=codex_home.expanduser().resolve(); user_home=user_home.expanduser().resolve()
    install_root=codex_home/"factory-os"/"1.1.0"
    report=LifecycleReport("cleanup-apply" if apply else "cleanup-dry-run",str(codex_home),str(user_home),str(install_root))
    plan=load_plan(plan_path)
    allowed_roots=[codex_home, user_home/".agents"/"skills"]
    quarantine=codex_home/"factory-os-quarantine"/datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if apply:
        backup=create_backup(codex_home,user_home,backup_base); report.backup_path=str(backup)
        report.add("backup","ok",str(backup),"Created pre-cleanup backup.")

    for idx,op in enumerate(plan["operations"]):
        if not isinstance(op,dict):
            report.add("cleanup","blocked",detail=f"Operation {idx} is not an object."); continue
        kind=str(op.get("op","")); src=Path(str(op.get("path",""))).expanduser()
        if kind not in ALLOWED_OPS:
            report.add(kind or "cleanup","blocked",str(src),"Unsupported mutation. Phase 6 cleanup intentionally permits only reversible quarantine/restore operations."); continue
        if not any(_inside(src,r) for r in allowed_roots):
            report.add(kind,"blocked",str(src),"Path is outside governed Codex/skill roots."); continue
        if kind=="quarantine_path":
            if not src.exists():
                report.add(kind,"skipped",str(src),"Path does not exist."); continue
            rel = src.resolve().relative_to(next(r for r in allowed_roots if _inside(src,r)).resolve())
            bucket = "codex" if _inside(src,codex_home) else "skills"
            dst=quarantine/bucket/rel
            if not apply:
                report.add(kind,"ok",str(src),f"DRY RUN: would move to {dst}"); continue
            dst.parent.mkdir(parents=True,exist_ok=True); shutil.move(str(src),str(dst))
            report.add(kind,"ok",str(src),f"Moved to reversible quarantine: {dst}", quarantine_path=str(dst))
        elif kind=="restore_path":
            dst=Path(str(op.get("destination",""))).expanduser()
            if not src.exists():
                report.add(kind,"blocked",str(src),"Quarantined source not found."); continue
            if not any(_inside(dst,r) for r in allowed_roots):
                report.add(kind,"blocked",str(dst),"Restore destination is outside governed roots."); continue
            if dst.exists():
                report.add(kind,"blocked",str(dst),"Restore destination already exists; refusing overwrite."); continue
            if not apply:
                report.add(kind,"ok",str(src),f"DRY RUN: would restore to {dst}"); continue
            dst.parent.mkdir(parents=True,exist_ok=True); shutil.move(str(src),str(dst))
            report.add(kind,"ok",str(dst),"Restored quarantined resource.")
    return report

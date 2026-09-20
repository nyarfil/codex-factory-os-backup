from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

from .hooks import FACTORY_TOKEN, load_hooks
from .integration import govern_environment
from .managed_block import BEGIN, END
from .manifest import load_manifest
from .models import LifecycleReport
from .fsutil import sha256_file


def _codex_version() -> tuple[str | None, str | None]:
    exe=shutil.which("codex")
    if not exe:
        return None, None
    try:
        p=subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=5)
        return exe, (p.stdout or p.stderr).strip()
    except Exception as exc:
        return exe, f"error: {exc}"


def doctor(codex_home: Path, user_home: Path, version: str = "1.1.0", *,
           source_root: Path | None = None, repo_root: Path | None = None) -> LifecycleReport:
    codex_home=codex_home.expanduser().resolve(); user_home=user_home.expanduser().resolve()
    install_root=codex_home/"factory-os"/version
    report=LifecycleReport("doctor",str(codex_home),str(user_home),str(install_root))

    if sys.version_info >= (3,11):
        report.add("python", "ok", detail=f"Python {sys.version.split()[0]}")
    else:
        report.add("python", "warning", detail=f"Python {sys.version.split()[0]}; Python 3.11+ is recommended because Governor uses tomllib.")

    exe, ver=_codex_version()
    report.add("codex_cli", "ok" if exe else "warning", exe, ver or "Codex CLI not found on PATH; static checks only.")

    config=codex_home/"config.toml"
    if config.exists():
        if tomllib is None:
            report.add("config_parse", "warning", str(config), "tomllib unavailable.")
        else:
            try:
                with config.open("rb") as f: tomllib.load(f)
                report.add("config_parse", "ok", str(config), "config.toml parses successfully.")
            except Exception as exc:
                report.add("config_parse", "failed", str(config), str(exc))

    manifest=load_manifest(install_root)
    if manifest:
        report.add("manifest", "ok", str(install_root/"install-manifest.json"), "Install manifest present.")
    else:
        report.add("manifest", "warning", str(install_root), "Install manifest not found.")
    if manifest:
        changed=[]
        for item in manifest.get("managed_files",[]):
            p=Path(item.get("path","")); exp=item.get("sha256")
            if p.is_file() and exp and p.name not in {"AGENTS.md","AGENTS.override.md","hooks.json"} and sha256_file(p)!=exp:
                changed.append(str(p))
        report.add("managed_integrity", "warning" if changed else "ok", detail=f"Locally modified managed files: {changed}" if changed else "Managed agent/skill files match install fingerprints.")

    guidance_candidates=[codex_home/"AGENTS.override.md",codex_home/"AGENTS.md"]
    guidance=next((p for p in guidance_candidates if p.exists() and BEGIN in p.read_text(encoding="utf-8",errors="replace") and END in p.read_text(encoding="utf-8",errors="replace")),None)
    report.add("global_guidance", "ok" if guidance else "failed", str(guidance) if guidance else None, "Factory OS control-plane block is active." if guidance else "Factory OS control-plane block not found in global guidance.")

    agents=list((codex_home/"agents").glob("*.toml")) if (codex_home/"agents").exists() else []
    expected=list((install_root/"02-agents"/"agents").glob("*.toml")) if (install_root/"02-agents"/"agents").exists() else []
    missing=[p.name for p in expected if not (codex_home/"agents"/p.name).exists()]
    report.add("agents", "ok" if expected and not missing else "warning", str(codex_home/"agents"), f"Expected {len(expected)} Factory agents; missing={missing}")

    expected_skills=[p.name for p in (install_root/"03-skills"/"skills").iterdir()] if (install_root/"03-skills"/"skills").exists() else []
    missing_skills=[n for n in expected_skills if not (user_home/".agents"/"skills"/n/"SKILL.md").exists()]
    report.add("skills", "ok" if expected_skills and not missing_skills else "warning", str(user_home/".agents"/"skills"), f"Expected {len(expected_skills)} Factory skills; missing={missing_skills}")

    hooks_path=codex_home/"hooks.json"
    try:
        hooks=load_hooks(hooks_path)
        flat=json.dumps(hooks)
        active=FACTORY_TOKEN in flat or ("factory-os" in flat.lower() and "04-runtime" in flat.lower())
        report.add("hooks", "ok" if active else "warning", str(hooks_path), "Factory lifecycle hooks found." if active else "Factory lifecycle hooks not found.")
    except Exception as exc:
        report.add("hooks", "failed", str(hooks_path), str(exc))

    # Governor audit is advisory but important before/after cleanup.
    try:
        src = source_root or install_root
        gov=govern_environment(codex_home,user_home,repo_root,src)
        severe=[f for f in gov.findings if f.severity in {"high","critical"}]
        report.add("governor", "warning" if severe else "ok", detail=f"{len(gov.resources)} resources; {len(gov.findings)} findings; {len(severe)} high/critical.", severe=[f.code for f in severe])
    except Exception as exc:
        report.add("governor", "warning", detail=f"Governor scan unavailable: {exc}")

    return report

from __future__ import annotations

import json
import shutil
from pathlib import Path

from .backup import create_backup
from .fsutil import copy_file_atomic, copy_tree, sha256_file
from .hooks import load_hooks, merge_factory_hooks
from .integration import govern_environment
from .fsutil import atomic_write_json
from .managed_block import BEGIN, END, apply_block
from .manifest import build_manifest, load_manifest, write_manifest
from .models import LifecycleReport

VERSION = "1.1.0"


class InstallError(RuntimeError):
    pass


def _validate_source_bundle(source_root: Path, report: LifecycleReport) -> bool:
    required = [
        "01-router/factory_router/models.py", "01-router/factory_router/policy.py", "01-router/factory_router/router.py",
        "02-agents/catalog/agent_catalog.json", "03-skills/catalog/factory_skill_map.json",
        "04-runtime/config/hooks.json", "05-governor/factory_governor/governor.py",
        "06-lifecycle/templates/AGENTS.factory-os.md",
    ]
    missing = [x for x in required if not (source_root / x).is_file()]
    agent_count = len(list((source_root / "02-agents" / "agents").glob("*.toml")))
    skills = [d for d in (source_root / "03-skills" / "skills").glob("factory-*") if (d / "SKILL.md").is_file()]
    hook_names = {"session_start.py","user_prompt_submit.py","pre_tool_use_agent.py","subagent_start.py","subagent_stop.py"}
    existing_hooks = {p.name for p in (source_root / "04-runtime" / "hooks").glob("*.py")}
    if missing or agent_count < 24 or len(skills) != 6 or not hook_names.issubset(existing_hooks):
        report.add("source_bundle", "blocked", str(source_root),
                   "Factory OS source bundle is incomplete; refusing partial installation.",
                   missing=missing, agent_count=agent_count, skill_count=len(skills),
                   missing_hooks=sorted(hook_names-existing_hooks))
        return False
    report.add("source_bundle", "ok", str(source_root),
               f"Source bundle complete: {agent_count} agents, {len(skills)} entry skills, required runtime/hooks present.")
    return True


def _guidance_source(source_root: Path) -> str:
    template = source_root / "06-lifecycle" / "templates" / "AGENTS.factory-os.md"
    return template.read_text(encoding="utf-8")


def _effective_global_guidance(codex_home: Path) -> Path:
    override = codex_home / "AGENTS.override.md"
    return override if override.exists() else codex_home / "AGENTS.md"


def _is_factory_owned_text(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    return "codex factory os" in text or "factory os control plane" in text


def _preflight(source_root: Path, codex_home: Path, user_home: Path, install_root: Path,
               report: LifecycleReport, force: bool) -> bool:
    """Return True only when mutation is safe to start."""
    problems = 0
    if install_root.exists() and not force:
        report.add("preflight_install_root", "blocked", str(install_root),
                   "Factory OS is already installed. Use update or --force.")
        problems += 1

    guidance = _effective_global_guidance(codex_home)
    if guidance.exists():
        text = guidance.read_text(encoding="utf-8", errors="replace")
        if (BEGIN in text) ^ (END in text):
            report.add("preflight_guidance", "blocked", str(guidance),
                       "Found only one Factory OS managed-block marker; refusing to guess the intended boundary.")
            problems += 1

    for src in sorted((source_root / "02-agents" / "agents").glob("*.toml")):
        dst = codex_home / "agents" / src.name
        if dst.exists() and sha256_file(dst) != sha256_file(src) and not _is_factory_owned_text(dst) and not force:
            report.add("preflight_agent", "blocked", str(dst),
                       "Same-name custom agent exists and is not Factory OS-owned.")
            problems += 1

    for src_dir in sorted((source_root / "03-skills" / "skills").iterdir()):
        if not src_dir.is_dir():
            continue
        dst = user_home / ".agents" / "skills" / src_dir.name
        skill_md = dst / "SKILL.md"
        if dst.exists() and not _is_factory_owned_text(skill_md) and not force:
            report.add("preflight_skill", "blocked", str(dst),
                       "Same-name global skill exists and is not Factory OS-owned.")
            problems += 1

    hooks_path = codex_home / "hooks.json"
    if hooks_path.exists():
        try:
            load_hooks(hooks_path)
        except Exception as exc:
            report.add("preflight_hooks", "blocked", str(hooks_path),
                       f"Existing hooks.json is invalid; refusing to rewrite it: {exc}")
            problems += 1
    return problems == 0


def _copy_managed_file(src: Path, dst: Path, report: LifecycleReport) -> None:
    copy_file_atomic(src, dst)
    report.add("copy_managed", "ok", str(dst), "Installed managed file.")


def install(source_root: Path, codex_home: Path, user_home: Path, *, force: bool = False,
            backup_base: Path | None = None) -> LifecycleReport:
    source_root = source_root.resolve()
    codex_home = codex_home.expanduser().resolve()
    user_home = user_home.expanduser().resolve()
    install_root = codex_home / "factory-os" / VERSION
    report = LifecycleReport("install", str(codex_home), str(user_home), str(install_root))
    codex_home.mkdir(parents=True, exist_ok=True)

    if not _validate_source_bundle(source_root, report):
        return report

    # Full preflight before any managed mutation. A conflict must leave the environment untouched.
    if not _preflight(source_root, codex_home, user_home, install_root, report, force):
        return report

    backup = create_backup(codex_home, user_home, backup_base)
    report.backup_path = str(backup)
    report.add("backup", "ok", str(backup), "Created pre-install backup.")

    # Governance-first bootstrap: capture the user's current customization before adding Factory OS.
    try:
        before = govern_environment(codex_home, user_home, source_root=source_root)
        audit_path = backup / "governance-before.json"
        atomic_write_json(audit_path, before.to_dict())
        severe = [f for f in before.findings if f.severity in {"high", "critical"}]
        report.add("governance_before", "warning" if severe else "ok", str(audit_path),
                   f"Captured pre-install inventory: {len(before.resources)} resources, {len(before.findings)} findings, {len(severe)} high/critical.")
    except Exception as exc:
        report.add("governance_before", "warning", detail=f"Pre-install Governor scan failed; installation can continue because the backup already exists: {exc}")

    if install_root.exists():
        shutil.rmtree(install_root)
    install_root.parent.mkdir(parents=True, exist_ok=True)
    install_root.mkdir(parents=True, exist_ok=False)
    for phase in ("01-router", "02-agents", "03-skills", "04-runtime", "05-governor", "06-lifecycle"):
        src = source_root / phase
        dst = install_root / phase
        copy_tree(src, dst, ignore_names={"__pycache__", ".pytest_cache"})
    report.add("install_root", "ok", str(install_root), "Installed versioned Factory OS runtime.")

    managed_paths: list[Path] = []
    guidance_path = _effective_global_guidance(codex_home)
    apply_block(guidance_path, _guidance_source(source_root))
    managed_paths.append(guidance_path)
    report.add("global_guidance", "ok", str(guidance_path),
               "Inserted/updated bounded Factory OS control-plane block.")

    agent_dst = codex_home / "agents"
    agent_dst.mkdir(parents=True, exist_ok=True)
    for src in sorted((source_root / "02-agents" / "agents").glob("*.toml")):
        dst = agent_dst / src.name
        _copy_managed_file(src, dst, report)
        managed_paths.append(dst)

    skill_dst_root = user_home / ".agents" / "skills"
    skill_dst_root.mkdir(parents=True, exist_ok=True)
    for src_dir in sorted((source_root / "03-skills" / "skills").iterdir()):
        if not src_dir.is_dir():
            continue
        dst_dir = skill_dst_root / src_dir.name
        if dst_dir.exists():
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
        report.add("copy_skill", "ok", str(dst_dir), "Installed Factory entry skill.")
        managed_paths.extend(x for x in dst_dir.rglob("*") if x.is_file())

    hooks_path = codex_home / "hooks.json"
    try:
        changed, removed = merge_factory_hooks(hooks_path, install_root)
        managed_paths.append(hooks_path)
        report.add("hooks", "ok", str(hooks_path),
                   f"Merged Factory OS hooks; replaced {removed} previous Factory hook group(s)." if changed else "Hooks already current.")
    except Exception as exc:  # should have been caught by preflight; retain fail-safe reporting
        report.add("hooks", "failed", str(hooks_path), f"Could not merge hooks: {exc}")

    config_path = codex_home / "config.toml"
    if config_path.exists() and "[hooks" in config_path.read_text(encoding="utf-8", errors="replace"):
        report.add("mixed_hooks", "warning", str(config_path),
                   "Inline hooks and hooks.json will coexist. Codex merges both and warns; normalize later with Governor cleanup.")

    manifest = build_manifest(VERSION, install_root, managed_paths, codex_home, user_home,
                              guidance_path, hooks_path)
    manifest_path = write_manifest(install_root, manifest)
    report.add("manifest", "ok", str(manifest_path), "Wrote ownership/integrity manifest.")

    try:
        after = govern_environment(codex_home, user_home, source_root=install_root)
        audit_path = install_root / "governance-after.json"
        atomic_write_json(audit_path, after.to_dict())
        severe = [f for f in after.findings if f.severity in {"high", "critical"}]
        report.add("governance_after", "warning" if severe else "ok", str(audit_path),
                   f"Captured post-install inventory: {len(after.resources)} resources, {len(after.findings)} findings, {len(severe)} high/critical.")
    except Exception as exc:
        report.add("governance_after", "warning", detail=f"Post-install Governor scan failed: {exc}")
    return report


def update(source_root: Path, codex_home: Path, user_home: Path, *, force: bool = False,
           backup_base: Path | None = None) -> LifecycleReport:
    codex_home = codex_home.expanduser().resolve()
    install_root = codex_home / "factory-os" / VERSION
    current = load_manifest(install_root)
    report = LifecycleReport("update", str(codex_home), str(user_home.expanduser().resolve()), str(install_root))
    if current:
        modified=[]
        for item in current.get("managed_files", []):
            p=Path(item.get("path", ""))
            expected=item.get("sha256")
            if p.is_file() and expected and sha256_file(p) != expected:
                if p.name not in {"AGENTS.md", "AGENTS.override.md", "hooks.json"}:
                    modified.append(str(p))
        if modified and not force:
            report.add("integrity", "blocked",
                       detail="Managed files have local modifications; update refused without --force.",
                       modified=modified)
            return report
    result = install(source_root, codex_home, user_home, force=True if current else force,
                     backup_base=backup_base)
    result.operation = "update"
    return result

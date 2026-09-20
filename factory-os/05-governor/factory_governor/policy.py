from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from .models import Finding, Resource

CONTROL_PLANE_TERMS = {
    "model routing": "Model routing belongs to Factory OS.",
    "select the model": "Model selection belongs to Factory OS.",
    "always use astra": "Hard-wired model mandates bypass adaptive routing.",
    "always use sol": "Hard-wired model mandates bypass adaptive routing.",
    "disable factory": "Factory lifecycle control belongs to Factory OS.",
    "ignore agents.md": "Resources may not discard higher-level guidance.",
    "ignore previous instructions": "Resources may not attempt instruction takeover.",
    "spawn as many": "Unbounded fan-out conflicts with scheduler governance.",
    "never use subagents": "Subagent policy belongs to Factory OS.",
}

BROAD_SHELL_PATTERNS = (
    r'pattern\s*=\s*\[\s*["\'](?:bash|sh|zsh|powershell|pwsh|cmd)["\']\s*\]',
    r'pattern\s*=\s*\[\s*["\'](?:bash|sh|zsh)["\']\s*,\s*["\']-c["\']',
    r'pattern\s*=\s*\[\s*["\'](?:bash|sh|zsh)["\']\s*,\s*["\']-lc["\']',
    r'pattern\s*=\s*\[\s*["\'](?:powershell|pwsh)["\']\s*,\s*["\']-Command["\']',
    r'pattern\s*=\s*\[\s*["\']cmd["\']\s*,\s*["\']/c["\']',
)


def _text(resource: Resource) -> str:
    try:
        return Path(resource.path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _dup_findings(resources: list[Resource], kind: str, code: str, noun: str) -> list[Finding]:
    grouped: dict[str, list[Resource]] = defaultdict(list)
    for r in resources:
        if r.kind == kind:
            grouped[r.name.strip().lower()].append(r)
    out: list[Finding] = []
    for name, items in grouped.items():
        if name and len(items) > 1:
            out.append(Finding(
                code=code,
                severity="medium",
                summary=f"Duplicate {noun} name: {items[0].name}",
                resource_ids=[r.id for r in items],
                rationale="Duplicate logical names make selection, shadowing, and ownership ambiguous.",
                disposition="merge",
                action="Choose one canonical owner/name or explicitly document intended scope-specific shadowing.",
            ))
    return out


def analyze(resources: list[Resource]) -> list[Finding]:
    findings: list[Finding] = []

    findings.extend(_dup_findings(resources, "skill", "DUPLICATE_SKILL", "skill"))
    findings.extend(_dup_findings(resources, "custom_agent", "DUPLICATE_AGENT", "custom agent"))
    findings.extend(_dup_findings(resources, "mcp", "DUPLICATE_MCP", "MCP server"))

    # Same Codex layer using both hooks.json and inline [hooks] is officially discouraged.
    by_scope = defaultdict(list)
    for r in resources:
        if r.kind == "hook":
            by_scope[r.scope].append(r)
    for scope, hooks in by_scope.items():
        fmts = {h.metadata.get("format") for h in hooks}
        if {"hooks.json", "config.toml"}.issubset(fmts):
            findings.append(Finding(
                code="MIXED_HOOK_FORMAT",
                severity="medium",
                summary=f"Both hooks.json and inline [hooks] are present in {scope} scope",
                resource_ids=[h.id for h in hooks],
                rationale="Codex merges both sources and warns; one source per layer is easier to govern and audit.",
                disposition="merge",
                action="Consolidate the layer onto one hook format during the later installer/cleanup phase.",
            ))

    # Parse failures must be visible.
    for r in resources:
        if r.metadata.get("parse_error"):
            findings.append(Finding(
                code="PARSE_ERROR",
                severity="high",
                summary=f"Could not parse {r.kind}: {r.name}",
                resource_ids=[r.id],
                rationale=str(r.metadata.get("parse_error")),
                disposition="quarantine_candidate",
                action="Repair syntax before integration; do not silently ignore this resource.",
            ))

    # Any subordinate text resource that tries to own routing/orchestration is a governance conflict.
    for r in resources:
        if r.kind not in {"agents_guidance", "skill", "custom_agent"} or r.ownership == "factory_os":
            continue
        text = _text(r).lower()
        hits = [term for term in CONTROL_PLANE_TERMS if term in text]
        if hits:
            findings.append(Finding(
                code="CONTROL_PLANE_TAKEOVER",
                severity="high",
                summary=f"Subordinate resource contains control-plane directives: {r.name}",
                resource_ids=[r.id],
                rationale="; ".join(CONTROL_PLANE_TERMS[h] for h in hits[:4]),
                disposition="quarantine_candidate",
                action="Move domain-specific content out of routing/orchestration directives or explicitly reconcile it with Factory OS policy.",
            ))

    # Broad out-of-sandbox shell allow rules are governance/security hazards.
    for r in resources:
        if r.kind != "rule":
            continue
        text = _text(r)
        if 'decision = "allow"' in text or "decision = 'allow'" in text:
            if any(re.search(pattern, text, flags=re.I | re.S) for pattern in BROAD_SHELL_PATTERNS):
                findings.append(Finding(
                    code="BROAD_SHELL_ALLOW",
                    severity="critical",
                    summary=f"Broad shell allow rule requires review: {r.name}",
                    resource_ids=[r.id],
                    rationale="Allowing a shell wrapper broadly can hide multiple commands behind one permitted prefix.",
                    disposition="quarantine_candidate",
                    action="Replace with narrow executable/argument prefixes and test with `codex execpolicy check`.",
                ))

    # Many implicit global skills increase ambiguity and discovery overhead.
    global_skills = [r for r in resources if r.kind == "skill" and r.scope == "global"]
    if len(global_skills) > 24:
        findings.append(Finding(
            code="GLOBAL_SKILL_SPRAWL",
            severity="medium",
            summary=f"Large global skill surface: {len(global_skills)} skills",
            resource_ids=[r.id for r in global_skills],
            rationale="A large always-discoverable skill set increases routing ambiguity and context pressure.",
            disposition="review",
            action="Keep broadly reusable entry skills global; move project/domain-specific skills to project scope or disable unused skills.",
        ))

    # Excessive global MCP surface should be reviewed, not auto-removed.
    global_mcps = [r for r in resources if r.kind == "mcp" and r.scope == "global" and r.enabled is not False]
    if len(global_mcps) > 12:
        findings.append(Finding(
            code="GLOBAL_MCP_SPRAWL",
            severity="medium",
            summary=f"Large global MCP surface: {len(global_mcps)} configured servers",
            resource_ids=[r.id for r in global_mcps],
            rationale="Always-available external tools expand startup cost, tool-selection ambiguity, and operational surface area.",
            disposition="review",
            action="Keep universal MCPs global; scope specialist MCPs to projects/factories when practical.",
        ))

    # Multiple global guidance files are legal only via override semantics, but deserve explicit ownership.
    global_guidance = [r for r in resources if r.kind == "agents_guidance" and r.scope == "global"]
    if len(global_guidance) > 1:
        findings.append(Finding(
            code="GLOBAL_GUIDANCE_OVERRIDE_PRESENT",
            severity="low",
            summary="Global AGENTS override chain is present",
            resource_ids=[r.id for r in global_guidance],
            rationale="Codex prefers AGENTS.override.md over AGENTS.md at the global layer; the effective control-plane source should be intentional.",
            disposition="review",
            action="Ensure the effective global guidance contains the Factory OS control-plane contract or remove stale overrides later.",
        ))

    return sorted(findings, key=lambda f: ({"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}[f.severity], f.code))

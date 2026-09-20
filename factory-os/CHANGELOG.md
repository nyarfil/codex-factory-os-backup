# Changelog

## 1.1.0-dev — 2026-09-20

### Completed

- Phase 01: deterministic Factory Router implemented and unit-tested.
- Phase 02: 31-role Custom Agent Library implemented as native Codex TOML + machine-readable JSON catalog.
- Added Software, CAD/3DP, Research, General, Data, and Document roles.
- Enforced Astra-as-bounded-read-only-specialist policy in Phase 02 tests.
- Added single-writer integration owners for Software and CAD/3DP.
- Added compatibility notes for Codex custom-agent/model-override runtime regressions.
- Added Phase 01 ↔ Phase 02 contract tests.
- Phase 03: six Factory Skills implemented with progressive-disclosure references.
- Added specialized Software workflows for implementation, debugging, architecture, review/verification, and delegation.
- Added specialized CAD/3DP workflows for geometry/CAD edits, mechanism design, FDM DFMA, simulation/optimization, verification, and delegation.
- Added Research, Data, Document, and explicit General fallback factories.
- Added Phase 01 ↔ Phase 02 ↔ Phase 03 contract tests.
- Phase 04: Codex App Server runtime probe implemented for `model/list` and `account/rateLimits/read`.
- Added conservative quota posture and Astra gating without inventing undocumented model-to-bucket mappings.
- Added runtime model/reasoning-effort resolver and fail-visible fallbacks.
- Added SessionStart, UserPromptSubmit, PreToolUse Agent/spawn, SubagentStart and SubagentStop hooks.
- Added subagent expected-vs-actual model audit against the Phase 02 Agent Catalog.
- Added JSONL fake App Server integration tests and fail-open no-Codex behavior.
- Phase 05: Codex Environment Governor implemented as a scan-only control-plane inventory and conflict analyzer.
- Declared Factory OS as the top-level user-managed Codex customization control plane; MCP/Rules/Skills/Agents/Hooks/project guidance are governed subordinate resources.
- Added inventory for global/project/nested AGENTS guidance, Skills, MCP servers, custom Agents, Hooks, Rules, and config files.
- Added ownership/scope metadata and SHA-256 fingerprints for file-backed resources.
- Added duplicate Skill/Agent/MCP detection, mixed-hook-format detection, parse-error surfacing, control-plane takeover detection, broad-shell-allow detection, and global surface-sprawl review findings.
- Phase 05 is intentionally non-destructive: no delete/disable/rename/rewrite operations.
- Phase 06: governance-first lifecycle/bootstrap manager implemented.
- Added full preflight before mutation, timestamped backups, pre/post Governor snapshots, versioned runtime installation, bounded global AGENTS managed block, custom-agent/Skill installation, Hook merge/removal, ownership manifest, update integrity guard, Doctor, and safe uninstallation.
- Added reversible cleanup executor with dry-run default and quarantine/restore operations only; arbitrary delete/TOML rewrite is intentionally excluded.
- Existing `config.toml`, MCPs, Rules, unrelated Skills/Agents, and unrelated Hook groups are preserved by bootstrap.
- Added Windows PowerShell lifecycle entrypoints.
- Final fresh-process validation after Phase 07 repair: **70/70 PASS** (Phase 01–07).

### Phase 07 final review / repair

- Re-read the physical workspace as source of truth and repaired missing Phase 01/04/05/06 modules and tests.
- Materialized all 31 native custom-agent TOMLs and all six Factory Skills with references.
- Corrected Codex hook output to the documented `hookSpecificOutput` format and added process-level hook contract tests.
- Added source-bundle completeness checks and preservation of locally modified managed resources on uninstall.
- Reduced persistent/per-turn context and tightened subagent fan-out for token efficiency.
- Added fresh-process distribution install/doctor/uninstall test and final static validation.
- Final Linux-container validation: **70/70 PASS**, zero missing relative imports, zero JSON/TOML parse errors, zero broken Skill references.

### Environment-dependent after installation

- Native Windows Codex smoke test, hook trust approval, actual account model/quota check, and reviewed cleanup of the user's real existing MCP/Rules/Skills remain machine-specific post-install checks.

> Earlier draft documentation described some planned Phase 03–06 features as if they were already implemented. This changelog and the current README supersede those draft claims.

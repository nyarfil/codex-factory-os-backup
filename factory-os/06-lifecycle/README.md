# Phase 06 — Lifecycle / Bootstrap / Safe Cleanup

Phase 06 turns Phases 01–05 into a **safe installable lifecycle unit** without yet declaring the whole project production-ready. It is designed for the user's stated bootstrap order: Factory OS is installed first, then it inventories and governs the existing Codex customization surface before later cleanup/reorganization.

## Responsibilities

- preflight all Factory OS-owned names before mutation;
- create a backup before install, uninstall, or cleanup apply;
- capture a pre-install Governor inventory;
- install a versioned Factory OS runtime under `~/.codex/factory-os/1.1.0/`;
- inject a bounded control-plane block into the **effective global** `AGENTS` file;
- install Factory custom agents under `~/.codex/agents/`;
- install Factory entry Skills under `~/.agents/skills/`;
- merge Factory lifecycle Hooks into `~/.codex/hooks.json` without replacing unrelated hook groups;
- preserve `config.toml`, existing MCPs, Rules, unrelated Skills/Agents, and unrelated Hooks;
- write an ownership/integrity manifest;
- run Doctor checks after installation;
- support safe updates and bounded uninstallation;
- execute reviewed cleanup plans in **dry-run by default**;
- make cleanup reversible by moving resources to quarantine rather than deleting them.

## Bootstrap order

```text
Existing Codex environment
        │
        ▼
Phase 06 preflight
        │
        ├─ name collision check
        ├─ malformed managed-marker check
        └─ hooks.json parse check
        │
        ▼
Full backup
        │
        ▼
Phase 05 Governor scan (BEFORE)
        │
        ▼
Install Factory OS control plane
        │
        ├─ global AGENTS managed block
        ├─ custom agents
        ├─ Factory Skills
        ├─ runtime + hooks
        └─ ownership manifest
        │
        ▼
Phase 05 Governor scan (AFTER)
        │
        ▼
Doctor
        │
        ▼
Reviewed cleanup plan
        │
        ▼
Dry-run → quarantine/apply → re-scan
```

## Why the global AGENTS file is patched instead of replaced

Codex builds an instruction chain from global guidance plus project-local guidance. If `~/.codex/AGENTS.override.md` exists, it is the effective global guidance file ahead of `AGENTS.md`. Phase 06 therefore inserts one bounded Factory OS block into the effective global file instead of replacing user content.

Markers:

```text
<!-- CODEX_FACTORY_OS:BEGIN -->
...
<!-- CODEX_FACTORY_OS:END -->
```

Update replaces only that block. Uninstall removes only that block.

## Conflict policy

The installer performs a full preflight before changing managed resources. It refuses to overwrite:

- an unrelated same-name custom agent;
- an unrelated same-name Factory entry Skill;
- malformed Factory managed-block boundaries;
- an invalid existing `hooks.json`.

A blocked preflight leaves the actual Codex configuration untouched.

## Hooks

Factory hook groups are merged into `~/.codex/hooks.json`. Existing hook groups remain present. Factory groups carry a `factory-os-managed` status marker so uninstall can remove only Factory-owned hook groups.

If the user already has inline `[hooks]` inside `config.toml`, Phase 06 **does not rewrite that TOML**. Codex officially merges inline hooks and `hooks.json` but warns when both formats exist at the same layer. Phase 06 reports this as a cleanup item instead of attempting a risky automatic TOML migration.

## Cleanup executor

Phase 06 deliberately limits automatic cleanup to reversible operations:

- `quarantine_path`
- `restore_path`

It does **not** implement a generic `delete`, arbitrary TOML rewrite, or blind MCP removal. The user's existing MCP/Rules/Skills are valuable input to the Governor, and destructive cleanup requires a reviewed plan based on the actual environment.

The default is always dry-run. `--apply` is required for mutation and a backup is created before mutation.

## Doctor

Doctor checks:

- Python runtime;
- Codex CLI presence/version when available;
- `config.toml` parse health;
- install manifest;
- active global control-plane block;
- expected Factory custom agents;
- expected Factory entry Skills;
- active Factory hooks;
- Phase 05 Governor findings.

The current CI/container does not have the user's live Windows Codex environment, so the live Codex smoke test belongs to Phase 07.

## PowerShell entrypoints

Windows wrappers are in `scripts/`:

- `install.ps1`
- `update.ps1`
- `doctor.ps1`
- `uninstall.ps1`

They invoke the Python lifecycle package. The finished project should only be installed after Phase 07 packages and validates the complete distribution.

## Validation

Phase 06 unit/contract tests: **8 PASS**.

Combined Phase 01–06 test suite: **66 PASS**.

Tests include simulated user homes containing pre-existing AGENTS guidance, MCP config, Hooks, Skills, and custom Agents. They verify preservation across install/uninstall and verify cleanup quarantine/restore behavior.

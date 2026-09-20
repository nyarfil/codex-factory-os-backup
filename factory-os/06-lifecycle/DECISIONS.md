# Phase 06 design decisions

## D1 — Factory OS bootstrap is governance-first

Factory OS is intended to be the first top-level user-managed Codex control plane. Installation therefore captures the existing customization state before changing it, rather than assuming a clean environment.

## D2 — Preflight before mutation

Name collisions, malformed markers, and invalid hook JSON must be found before copying managed files. A failed preflight must not leave a half-installed control plane.

## D3 — Backup before every mutating lifecycle action

Install, uninstall, and cleanup apply create a timestamped backup first. Backups include global Codex guidance/config/hooks and the current custom-agent/rule/global-skill surfaces.

## D4 — Bounded ownership

Factory OS does not own the entire `~/.codex` tree. It owns only:

- its versioned runtime;
- its bounded AGENTS block;
- its named Factory agent files;
- its named Factory Skill directories;
- its marked Hook groups;
- its install manifest/audit outputs.

## D5 — Do not rewrite existing `config.toml` during bootstrap

The user's MCPs, project trust settings, profiles, and other configuration may already be valuable. Phase 06 does not normalize or regenerate the file. This prevents a bootstrap tool from becoming the source of configuration loss.

## D6 — Mixed hook formats are surfaced, not silently migrated

Codex merges `hooks.json` and inline `[hooks]`, but warns when both occur at one layer. Automatically translating arbitrary user TOML would be riskier than temporarily tolerating the warning. Governor reports the issue for reviewed cleanup.

## D7 — Cleanup is reversible by construction

The generic cleanup executor supports quarantine/restore, not delete. Embedded configuration resources such as MCP entries are not blindly edited by Phase 06. Their final disposition should be derived from the actual Phase 05 inventory during Phase 07/user-environment cleanup.

## D8 — Update protects local changes

Managed files are fingerprinted. Update refuses to overwrite locally changed managed files unless `--force` is explicitly used. AGENTS and Hooks are merge-managed and therefore treated separately.

## D9 — Runtime is versioned

Runtime files live below `~/.codex/factory-os/<version>/`. Hooks point at the installed version. This makes ownership explicit and provides a clean basis for future version migrations.

## D10 — Live Codex is a Phase 07 gate

Passing unit/simulated-home tests is necessary but not sufficient. Final packaging is blocked until the completed system is tested with a real Codex CLI/App Server on the target Windows environment.

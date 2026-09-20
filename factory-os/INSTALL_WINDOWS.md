# Windows installation / first cleanup

## Prerequisites

- Windows 11
- Codex CLI / IDE / desktop environment installed and signed in
- Python 3.11+ recommended (`py -3.11` or `python`)
- Extract this ZIP to a normal writable folder

The installer intentionally does not bypass Codex hook trust.

## 1. Install Factory OS first

PowerShell:

```powershell
cd <extracted-folder>
.\install.ps1
```

The installer will:

1. validate that this distribution is complete;
2. preflight collisions;
3. back up current Codex customization;
4. inventory the pre-install environment;
5. install versioned runtime under `~/.codex/factory-os/1.1.0/`;
6. add a bounded Factory OS block to the effective global AGENTS file;
7. install Factory custom agents and entry Skills;
8. merge Factory hooks without deleting unrelated hooks;
9. create an ownership manifest;
10. inventory the post-install environment.

If a dangerous collision exists, installation stops before managed mutation.

## 2. Restart Codex and trust hooks

In Codex, run:

```text
/hooks
```

Review the Factory OS hooks and trust them if they match this package. Codex ties trust to the hook definition hash, so changed hooks may require re-review.

## 3. Doctor

```powershell
.\doctor.ps1
```

Warnings about live model availability should be resolved in the actual Codex environment. Static tests cannot substitute for this step.

## 4. Inventory your existing customization

```powershell
.\govern.ps1 --md-out governance.md --json-out governance.json
```

This is scan-only. It does not delete anything.

Review especially:

- duplicate Skills or custom agents;
- duplicated MCP names across scopes;
- conflicting model-routing instructions in old Skills/AGENTS;
- broad shell allow rules;
- mixed hooks.json / inline hook configuration;
- globally installed specialist Skills/MCPs that should be project-scoped.

## 5. Cleanup

Factory OS cleanup is deliberately reversible. Create a reviewed JSON plan using `quarantine_path`; run dry-run first, then `--apply` only after review.

Do not blindly remove MCP entries embedded in `config.toml`. Reconcile those from the Governor report.

## 6. Optional config recommendations

`06-lifecycle/templates/recommended-config.toml` contains a suggested starting point:

- parent model: `gpt-5.6`
- default generic subagent: `gpt-5.6-terra` / medium
- normal maximum concurrent children: 4

The installer does **not** merge this automatically, because preserving the user's existing `config.toml` is safer than a lossy TOML rewrite.

## Update

```powershell
.\update.ps1
```

Update stops if a strict managed Agent/Skill file was locally modified unless the user deliberately resolves/forces it.

## Uninstall

```powershell
.\uninstall.ps1
```

Factory OS removes its managed block, hook groups, and unmodified managed Agent/Skill resources. Locally modified Factory resources are preserved and reported.

## Backup locations

Lifecycle operations create timestamped backups under the Codex home Factory backup directory by default. Keep at least the first pre-install backup until the cleanup of your old environment is complete.

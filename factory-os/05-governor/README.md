# Phase 05 — Codex Environment Governor

Phase 05 makes Factory OS the control plane for the user's Codex customization environment **without modifying the environment yet**.

## What it inventories

- global/project/nested `AGENTS.md` and `AGENTS.override.md`;
- global/project Skills;
- MCP servers from `config.toml`;
- global/project custom Agents;
- `hooks.json` and inline `[hooks]`;
- `.rules` execution-policy files;
- relevant `config.toml` files.

Every file-backed resource receives a SHA-256 fingerprint and scope/ownership metadata.

## What it detects

- duplicate skill names;
- duplicate custom-agent names;
- duplicate MCP server names across scopes;
- mixed `hooks.json` + inline hooks in the same scope;
- syntax/parse failures;
- subordinate resources attempting to own model routing/orchestration;
- broad shell `allow` execution rules;
- unusually large global Skill or MCP surfaces;
- ambiguous global AGENTS override chains.

## Control-plane rule

Factory OS owns global model routing, factory selection, delegation policy, quota/cost posture, cross-factory integration, and escalation. Other customization assets remain useful, but are governed resources beneath it.

Codex's platform/admin/security constraints and native precedence remain authoritative. Factory OS does not pretend to create a new hard Codex precedence tier; it audits and reconciles user-managed assets so they behave as subordinates in practice.

## Usage (development standalone)

```bash
python -m factory_governor.cli \
  --codex-home ~/.codex \
  --user-home ~ \
  --repo /path/to/repo \
  --json-out governance.json \
  --md-out governance.md
```

The command is read-only. It does not delete or disable anything.

## Output dispositions

- `keep`
- `review`
- `merge`
- `disable_candidate`
- `quarantine_candidate`

They are recommendations only in this phase.

## Tests

The tests construct isolated fake Codex/user/repository trees and verify inventory, duplicate/conflict detection, takeover detection, broad-rule detection, hashing, and scan-only behavior.

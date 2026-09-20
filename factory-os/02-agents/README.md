# Codex Factory OS — Phase 2: Custom Agent Library

This component is the **agent library only**. It does not install anything and it does not yet connect to the Phase 1 router.

## Purpose

Provide a reusable user-level catalog for `~/.codex/agents/*.toml` with explicit specialization, model tier, reasoning effort, and sandbox policy. The later integration phase will choose among these roles from the deterministic routing decision.

## Design rules

- **Luna**: cheap scouting/extraction/repository mapping.
- **Terra**: routine bounded implementation, tests, research, CAD execution.
- **Sol**: architecture, integration ownership, difficult debugging, mechanical reasoning, verification.
- **Astra**: scarce, bounded, usually **read-only** specialist for genuinely hard reasoning. It should normally hand implementation back to Sol/Terra.
- Read-only agents are deliberately common. Parallel exploration is cheap and low-conflict; overlapping writers are not.
- Agent TOMLs do **not** hard-code MCP servers or skills, so existing user/project tools can inherit from the parent Codex session.
- `software_integration_owner` and `cad_integration_owner` are the intended single-writer owners after parallel work.

## Contents

- `agents/` — Codex custom-agent TOMLs.
- `catalog/agent_catalog.json` — machine-readable source of truth for later Router/Hook integration.
- `catalog/route_agent_map.json` — Phase 1 task-type to preferred role mapping.
- `tests/test_agents.py` — schema/policy checks.
- `COMPATIBILITY.md` — runtime caveats and fallback requirements.
- `DECISIONS.md` — architecture decisions for this component.

## Status

This phase is intentionally usable as a **library artifact**, not yet as a live installer. Phase 4/5 will handle runtime probing, compatibility fallback, installation, and user configuration merging.

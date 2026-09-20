# Phase 4 — Runtime Hooks, Model/Quota Probe, and Compatibility Layer

Phase 4 turns the static Factory OS design into a runtime-aware layer without yet installing it into `~/.codex`.

## Responsibilities

1. **Runtime model discovery** — query Codex App Server `model/list` instead of assuming a model exists.
2. **Quota posture** — query `account/rateLimits/read` and classify only the supported general usage snapshot as `green / amber / red / exhausted / unknown`.
3. **Runtime resolution** — reconcile a Phase 1 route with models and reasoning efforts actually reported by the running account/client.
4. **Always-on hook activation** — `SessionStart` and `UserPromptSubmit` inject short Factory OS routing invariants.
5. **Subagent model audit** — compare Phase 2's expected model for a custom agent with the model reported by `SubagentStart` / `SubagentStop`.
6. **Spawn guardrail** — `PreToolUse` matches `Agent|spawn_agent`, records the spawn, and reinforces bounded parallelism/single-writer rules.
7. **Fail-open behavior** — failure to probe quota/model state must not block ordinary Codex use.

## Deliberate limits

- The runtime does **not** infer an undocumented mapping from every model to an opaque quota bucket. Codex exposes quota snapshots, but an explicit model-to-bucket mapping is not guaranteed.
- Hooks are treated as guardrails, not the sole enforcement boundary.
- The `PreToolUse` spawn hook does not pretend it can always inspect the child task text; current multi-agent implementations can hide/encrypt that argument.
- The probe never starts a model turn and never consumes reset credits.
- Automatic installation/trust of hooks is Phase 5. This phase only supplies the tested files.

## Runtime files

- `factory_runtime/appserver.py` — JSONL App Server client/probe.
- `factory_runtime/quota_policy.py` — conservative quota posture and Astra gating.
- `factory_runtime/resolver.py` — route → actually available model/effort reconciliation.
- `factory_runtime/classifier.py` — cheap factory hint for `UserPromptSubmit` only; not the final router.
- `factory_runtime/audit.py` — append-only runtime audit log.
- `hooks/*.py` — lifecycle hooks.
- `config/hooks.json` — installation template used later by Phase 5.

## Operational principle

`UserPromptSubmit` gives the parent a cheap *factory hint*. The parent still inspects the real task and uses Phase 1's TaskContract/Router for non-trivial work. Phase 4 then checks whether the requested model/effort is actually available and whether optional Astra use should be suppressed under quota pressure.

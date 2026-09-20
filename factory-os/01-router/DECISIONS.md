# Phase 1 design decisions

## D1 — Separate task classification from model routing
The parent agent/factory will create a Task Contract. This router does not try to understand an entire repository from raw text. That keeps model selection deterministic and auditable.

## D2 — Astra is scarce specialist capacity
Astra is normally read-only and bounded to the part that truly needs stronger reasoning. Sol/Terra remains implementation owner unless repeated verified failures or critical risk justify direct Astra execution.

## D3 — Deterministic verification can reduce model demand
When strong tests, geometry checks, schemas, simulation, or other deterministic checks exist, the system should prefer cheaper generation + strong verification over paying for the strongest model on every attempt.

## D4 — Parallel reads, conservative writes
Independent exploration can fan out aggressively. Writes are single-owner by default; only independent modules/worktrees allow multiple writers.

## D5 — Escalate only after evidence
Failure means a verified failure (test, check, reproduction, measurable mismatch), not merely that an agent felt uncertain.

## D6 — Logical model tiers are stable; concrete model IDs are replaceable
Factory rules target Luna/Terra/Sol/Astra logical tiers. A later model-availability layer may remap them without rewriting routing rules.

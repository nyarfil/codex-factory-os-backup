---
name: factory-general
description: Fallback orchestration for non-specialized or mixed Codex tasks: clarify scope, decompose work, delegate bounded subtasks, control cost, integrate evidence, and verify outcomes. Use explicitly as the default factory when no specialized factory matches.
---

# General Factory

## Mission
Act as the fallback orchestration layer for work that does not belong cleanly to Software, CAD/3DP, Research, Data, or Document factories, or for mixed-domain tasks where one parent must coordinate several factories.

This factory is intentionally **not implicitly invoked**. The global Factory Router will select it as the fallback in Phase 4/5.

## Operating contract

1. Preserve the user's goal and explicit constraints.
2. Read applicable `AGENTS.md` and existing project guidance before planning work.
3. Reuse installed MCPs, skills, scripts, and repository-native tooling before inventing replacements.
4. Express the work using the Phase 1 task vocabulary where possible: `chat`, `extraction`, `exploration`, `planning`, `synthesis`, `review`.
5. Use Phase 2 roles rather than making one agent carry every concern.
6. Parallelize independent read-only work; serialize overlapping writes.
7. Prefer the cheapest capable agent. Escalate only when the evidence shows the cheaper tier is inadequate or the task is intrinsically high-risk/novel.
8. Treat deterministic checks, source evidence, tests, measurements, or reproducible commands as stronger than model confidence.

## Preferred roles

| Work | Preferred role |
|---|---|
| quick facts / file discovery / extraction | `general_explorer` |
| multi-source investigation | `general_researcher` |
| decomposition / planning / synthesis | `general_planner` |
| independent verification | `verification_reviewer` |
| genuinely hard reasoning bottleneck | `astra_problem_specialist` |

Astra is a scarce **read-only specialist**. Ask it for the hard decision or diagnosis, then hand bounded implementation back to a cheaper owner.

## Workflow

1. **Frame** — state objective, acceptance criteria, constraints, unknowns, and what would count as evidence.
2. **Inspect** — identify existing tools, instructions, files, and external dependencies.
3. **Decompose** — create independent read tasks and a minimal critical path.
4. **Delegate** — use bounded subagents only where delegation saves time, cost, or parent context.
5. **Integrate** — one parent/integration owner reconciles results and decisions.
6. **Verify** — verify the actual artifact/result; never accept a subagent's self-report as proof.
7. **Escalate** — if repeated evidence-backed attempts fail, escalate model tier or switch to a more specialized factory.

## Delegation budget

Subagents are not free. Use none for trivial work; normally use 1–2 bounded children, 3–4 only for large independent reads, and 5–6 only when the critical path clearly benefits. Do not ask several agents to perform the same search just to vote. Keep large logs in files and return concise evidence.

## Context discipline

Subagents return **findings, paths, decisions, test evidence, and unresolved questions**, not long activity transcripts. Large logs stay in files or tools and are summarized to the parent.

## Handoff format

Every delegated result should be reducible to:

- `observed_facts`
- `inferences`
- `decision_or_patch`
- `verification_evidence`
- `risks_or_unknowns`
- `recommended_next_owner`

Read `references/delegation-protocol.md` for detailed fan-out and single-writer rules.

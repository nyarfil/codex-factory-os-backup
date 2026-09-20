---
name: factory-software
description: Software engineering factory for repositories, code changes, debugging, refactors, architecture, tests, migrations, APIs, build systems, and code review. Use for implementation work in source code; not for CAD/mechanical design.
---

# Software Factory

## Mission
Deliver correct, minimal, verifiable software changes while using Codex subagents and model tiers economically. Work from the real repository, build/test system, dependencies, and project instructions rather than generic architecture patterns.

## Entry checks

Before implementation:

1. Read applicable `AGENTS.md` and repository-local instructions.
2. Locate build/test/lint/type-check commands and package/lock files.
3. Discover existing MCPs, skills, scripts, code generators, and repository tooling relevant to the task. Reuse them rather than duplicating capability.
4. Map the actual execution path before changing unfamiliar code.
5. Classify the work with Phase 1 task types: `exploration`, `implementation`, `refactor`, `debug`, `testing`, `review`, `integration`, or `architecture`.

## Role routing

| Task | Default roles | Notes |
|---|---|---|
| exploration | `software_repo_mapper`, optionally `software_dependency_researcher` | cheap parallel read-only work |
| implementation | `software_builder`; use `software_senior_builder` for multi-file/high-reasoning changes | bounded writer |
| refactor | `software_senior_builder` | preserve behavior and compatibility |
| debug | `software_debugger`; escalate hard bottleneck to `software_astra_debug_specialist` | reproduce and falsify hypotheses |
| testing | `software_test_engineer` | independent where useful |
| architecture | `software_architect`; Astra only for genuinely hard/novel bottlenecks | architecture stays read-only until accepted |
| review | `software_reviewer` | review actual diff and call path |
| integration | `software_integration_owner` | final single-writer owner |

## Implementation workflow

1. **Map** the smallest relevant execution path and tests.
2. **Form a change contract**: intended behavior, invariants, files/areas likely affected, acceptance tests, compatibility requirements.
3. **Split independent investigations** among read-only agents when useful.
4. **Implement with one bounded owner** for overlapping files.
5. **Test cheaply first** (targeted tests/type checks), then broaden according to blast radius.
6. **Review independently** for correctness, concurrency, security, migrations, compatibility, and missing tests when the change warrants it.
7. **Integrate** parallel contributions through `software_integration_owner`.
8. **Escalate** only the unresolved reasoning bottleneck to Astra; do not send bulk coding to Astra by default.

## Delegation budget

Subagents are not free. Use none for trivial work; normally use 1–2 bounded children, 3–4 only for large independent reads, and 5–6 only when the critical path clearly benefits. Do not ask several agents to perform the same search just to vote. Keep large logs in files and return concise evidence.

## Failure discipline

For bugs, do not patch symptoms first. Reproduce when possible, build a causal chain, make falsifiable hypotheses, and add a regression test for the root cause. If two evidence-backed Sol-level attempts fail or the problem is intrinsically novel/high-risk, use the Astra debug specialist for diagnosis and hand implementation back afterward.

## Change discipline

- Keep diffs focused; avoid unrelated cleanup.
- Preserve public behavior unless the request changes it.
- Do not silently upgrade dependencies, rewrite architecture, or change persistent schemas without an explicit migration decision.
- Never claim tests passed unless they were actually run and their result is known.
- Treat existing user/project Skills and MCPs as assets; do not disable them merely because Factory OS is active.

## References

Read only what the task needs:
- `references/implementation.md` — bounded feature/change workflow.
- `references/debugging.md` — evidence-driven debugging.
- `references/architecture.md` — architecture and migrations.
- `references/review-verification.md` — review and test gates.
- `references/delegation.md` — parallelism and model handoff.

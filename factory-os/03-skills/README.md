# Codex Factory OS — Phase 3: Factory Skills

This component contains the **domain operating procedures** for Factory OS. It does not install them yet and does not depend on live hooks.

## Why six skills instead of dozens

Codex first loads Skill metadata (`name`, `description`, and path) and only loads a full `SKILL.md` after a Skill is selected. The initial Skill list has a context budget, so Factory OS deliberately exposes one entry Skill per factory and places detailed sub-workflows under `references/`.

Factories:

- `factory-general` — fallback/mixed-domain orchestration; implicit invocation disabled to avoid stealing specialized work.
- `factory-software` — codebase exploration, implementation, debugging, tests, architecture, review, integration.
- `factory-cad-3dp` — geometry, CAD edits, mechanism design, assemblies, FDM/3DP DFMA, simulation, optimization, verification.
- `factory-research` — source discovery, deep research, synthesis, fact checking.
- `factory-data` — structured-data analysis and quantitative verification.
- `factory-document` — document-centric writing/editing with source preservation.

## Relationship to earlier phases

- **Phase 1 Router** decides domain/task difficulty/model policy.
- **Phase 2 Agents** provide bounded specialized workers.
- **Phase 3 Skills** define *how work in each domain should be performed* and which Phase 2 roles are appropriate.

Phase 4 will add runtime hooks/probes. Phase 5 will install/merge everything. Until then these Skills are library artifacts only.

## Key design decisions

1. Skills do not hard-code MCP servers. Existing user/project MCPs and skills remain available through the parent session.
2. Software and CAD/3DP factories explicitly discover and reuse existing tooling rather than replacing it.
3. CAD/3DP does not assume the user's cadMCP is installed yet; when it becomes available, it is treated as an execution/knowledge backend under the factory.
4. Astra remains a read-only/high-cost specialist by policy; routine implementation and geometry execution stay with Terra/Sol.
5. Final correctness comes from tests, measurements, geometry checks, source evidence, or other deterministic verification—not subagent confidence.

## Validation

Run:

```bash
python 03-skills/tests/test_skills.py
python 03-skills/tests/test_phase_contracts.py
```

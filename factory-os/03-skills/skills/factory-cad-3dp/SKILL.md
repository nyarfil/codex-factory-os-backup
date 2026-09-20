---
name: factory-cad-3dp
description: Mechanical CAD and 3D-printing factory for STEP/STL/BRep geometry, parametric CAD edits, mechanisms, assemblies, tolerances, FDM/3DP DFMA, supports/orientation, simulation, and design verification. Use for physical part design; not ordinary software coding.
---

# CAD / 3DP Factory

## Mission
Turn physical requirements into manufacturable, verifiable geometry without asking the LLM to “eyeball” correctness. Separate design reasoning from deterministic CAD execution and from geometry/engineering verification.

This factory is tool-agnostic. If the user's cadMCP or another CAD MCP is present, discover and use it. If not, use the available CAD backend. **Do not assume a particular MCP exists and do not replace the user's CAD stack.**

## Entry checks

1. Identify source geometry and its authority: STEP/BRep, mesh/STL, scan, drawings, PCB/component solids, dimensions.
2. Preserve explicit protected geometry, interfaces, datum/reference frames, keep-out volumes, and user constraints.
3. Distinguish facts/measurements from assumptions and design decisions.
4. Inspect geometry with tools when available; do not infer exact dimensions from screenshots if CAD data exists.
5. Classify with Phase 1 task types: `geometry_inspection`, `cad_edit`, `cad_recipe`, `mechanism_design`, `dfm_3dp`, `simulation`, `optimization`, `review`, `integration`.

## Role routing

| Task | Default roles | Notes |
|---|---|---|
| geometry inspection | `cad_geometry_inspector` | read/measure first |
| reference structure research | `cad_reference_researcher` | existing mechanisms/parts/prior art |
| deterministic CAD edit/build | `cad_model_builder` | bounded writer/executor |
| CAD recipe/operation plan | `cad_recipe_engineer` | separate what/why from geometry operations |
| mechanism design | `cad_mechanism_engineer`; hard bottleneck → `cad_astra_mechanism_specialist` | force/DOF/return/stops/interfaces |
| FDM/3DP DFMA | `cad_3dp_dfm_engineer` | orientation/support/wall/layer load/process |
| simulation interpretation | `cad_simulation_analyst` | assumptions and boundary conditions matter |
| optimization | `cad_optimization_engineer`; Astra only for hard conceptual problem | optimization is constrained, not aesthetic |
| integration/review | `cad_integration_owner`, `verification_reviewer` | final single owner + independent evidence |

## Core workflow

1. **Measure/inspect** the source geometry and references.
2. **Compile requirements**: function, loads, motion, interfaces, clearances/tolerances, protected intent, manufacturing process, material/process assumptions, unknowns.
3. **Decompose function/behavior** before choosing shape for non-trivial mechanisms.
4. **Research/reference** existing proven structures when that reduces invention risk.
5. **Generate a small concept portfolio** for mechanism-level work; do not lock onto the first idea.
6. **Select with engineering criteria**: load path, DOF/constraints, assembly, manufacturability, failure modes, serviceability, space, cost/part count.
7. **Create a CAD recipe/plan** with references, features, operations, and verification targets.
8. **Execute geometry deterministically** with the available CAD tools.
9. **Measure the result**: validity, body count, bbox, clearances, interference, wall thickness, motion/stroke, reference consistency, and task-specific dimensions.
10. **Apply FDM/3DP checks** when printing is intended.
11. **Review and repair**; never substitute visual confidence for measurement.

## 3DP-specific rules

When the output is intended for FDM/3DP, explicitly consider:
- material and process envelope;
- nozzle/layer constraints if known;
- minimum walls/features appropriate to the actual printer/process;
- anisotropy and load direction relative to layers;
- overhang/bridge/support access and support-removal damage;
- tolerance/fit strategy and expected process variability;
- warping/shrinkage/thermal effects where relevant;
- print orientation versus strength, finish, dimensional accuracy, and support burden.

Do not invent numeric limits if printer/material/process evidence is missing. Mark them unknown or obtain the relevant profile/datasheet/test evidence.

## Delegation budget

Subagents are not free. Use none for trivial work; normally use 1–2 bounded children, 3–4 only for large independent reads, and 5–6 only when the critical path clearly benefits. Do not ask several agents to perform the same search just to vote. Keep large logs in files and return concise evidence.

## Astra use

Astra is for difficult **mechanical reasoning**, not routine boolean operations or dimension edits. Prefer:

`Astra specialist (read-only diagnosis/concept) → Sol mechanism/integration owner → Terra/Sol CAD builder → deterministic verification`.

## References

Read only the references needed by the current task:
- `references/geometry-and-cad-edit.md`
- `references/mechanism-design.md`
- `references/dfm-3dp.md`
- `references/simulation-optimization.md`
- `references/verification.md`
- `references/delegation.md`

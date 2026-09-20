---
name: forgecad-build-model
description: Build or edit `.forge.js` real product models through design, automatic/manual feedback gathering, inspection/simulation/FEA evidence, and iteration until ready.
forgecad-public: true
---

# Build Model

Create or edit ForgeCAD models through the loop that matters: design intent -> automatic or manual feedback gathering -> interpretation -> iteration -> readiness. Use the core `forgecad` skill as the source of truth for ForgeCAD API docs, generated API pages, CLI syntax, scene setup, assembly contracts, inspection bundles, FEA, simulation metadata, and examples. This skill defines the product-modeling workflow.

## Default Output Standard

Unless the user asks otherwise, build a **real product model**: an editable parametric CAD model of the actual physical product, machine, robot, fixture, part, assembly, or simulation asset the user asked for. The model should be closed, assembled, sourced, dimensioned, inspected, tested, and ready for the next real engineering loop.

Real product features are not optional polish. For every physical function the artifact needs, model the corresponding product evidence: wall thickness, fastener stacks, bosses, ribs, flanges, seats, gaskets, cable exits, service access, toleranced clearances, purchased parts, BOM entries, critical dimensions, simulation artifacts when behavior evidence matters, export artifacts when requested or process-dependent, and process-appropriate materials. If evidence is still missing, keep building or name the exact missing validation loop and residual risk; do not quietly lower the target quality.

Do not build a blurry visual facsimile unless the user explicitly asks for a
nonfunctional visual mockup. Avoid ambiguous labels such as "prototype" unless
you also state the intended readiness level and validation scope. A model that
looks plausible from one camera but fails sections, fit, connectivity, wall
thickness, motion, load path, or manufacturing review is not ready.

## File Placement

New `.forge.js` files go under date-based directories in the user's current ForgeCAD project or a clearly named local folder:

```text
YYYY/MM/DD/file.forge.js                         # tiny single-file model only
YYYY/MM/DD/folder/main.forge.js                  # central entry point for every multi-file build
YYYY/MM/DD/folder/NOTES.md                       # live build notes: learnings, API friction, surprises, follow-ups
YYYY/MM/DD/folder/docs/PRFAQ.md                  # product/user story and decision FAQ
YYYY/MM/DD/folder/docs/HLD.md                    # high-level design
YYYY/MM/DD/folder/docs/LLD-*.md                  # lower-level design docs as needed
YYYY/MM/DD/folder/docs/modules/*.md              # submodule or complex-part design notes
YYYY/MM/DD/folder/modules/<domain>/*.forge.js    # unified nested module tree: leaf modules to system modules
YYYY/MM/DD/folder/lib/*.js                       # pure helpers/constants, no geometry
```

- Use kebab-case descriptive names.
- Use `main.forge.js` as the central entry point. It should import high-level modules, not every leaf file in a huge build.
- Prefer one nested `modules/` tree, like software. Compose upward from leaf modules to larger modules to the system. Keep files small enough to understand and verify.
- Reusable `.forge.js` modules should return builder functions or module interfaces. Direct-run previews belong inside `if (require.main === module)`, like Python's `if __name__ == "__main__"`.
- Each module file must run standalone where practical and import via `require('./path/file.forge.js')`.
- Use plain `.js` only for constants, tables, and pure helpers. Do not put geometry in helper-only files.
- Keep `NOTES.md` current for non-trivial builds. Capture learnings, API frustrations, non-obvious modeling choices, inspection surprises, cleanup notes, and follow-up product/API ideas. Do not hide requirements or formal design decisions there; those belong in PRFAQ/HLD/LLD docs.
- Write as many markdown design files as the project needs. Complex parts and submodules deserve their own design notes; small edits may need only a short local note.

## Workflow

Keep the workflow current in the project docs. Do not advance a stage until its acceptance criteria pass, and expect to revisit earlier stages when feedback changes the design.

### Stage 1: Design Intent

Read `references/stage-1-design-intent.md`.

Accepted when the project has a product/user story, PR/FAQ or equivalent design-intent doc, output standard, process assumptions, explicit success criteria, and a first feedback plan.

### Stage 2: Architecture Plan

Read `references/stage-2-architecture-plan.md`.

Accepted when the HLD and needed LLD/module docs define the component graph, nested file structure, interfaces, parameters, build order, and evidence gates.

### Stage 3: Build Slices

Read `references/stage-3-build-slices.md`.

Accepted when each slice or module runs in isolation, exposes clean connectors/metadata, has targeted render/inspect evidence, and updates the design docs with findings.

### Stage 4: Feedback And Iteration

Read `references/stage-4-feedback-iteration.md`. Also read `references/inspection-feedback.md` for inspection bundles and `references/simulation-feedback.md` for MuJoCo, FEA, or other behavior checks.

Accepted only after automatic and manual evidence has been gathered, interpreted, and converted into model/design edits until the model behaves the way the user expects at the relevant module and system levels.

### Stage 5: Readiness Package

Read `references/stage-5-readiness-package.md`.

Accepted when the final post-iteration model passes run/render/inspect evidence, plus simulation or export evidence only when requested or process-critical, carries BOM and critical dimensions, and can be reported with evidence reviewed, residual risks, and the next validation loop if anything remains unproven.

## Reference Routing

Read only what the current stage needs:

- Stage references — the workflow acceptance gates.
- `references/parameter-controls.md` — deciding which user-facing `param()` controls to expose, where they live, and how to validate ranges.
- `references/module-contracts.md` — builder-first returns, preview guards, connector/data-flow rules, and assembly anti-patterns.
- `references/inspection-feedback.md` — choosing, running, and interpreting `forgecad inspect` evidence.
- `references/simulation-feedback.md` — MJCF/MuJoCo verification, FEA readiness, dynamic/contact checks, and behavior evidence.
- `references/readiness-review.md` — requirement checklist, evidence caps, and final readiness reporting.
- Core `forgecad` skill docs — API calls, CLI command syntax, generated assembly/viewport/scene/export docs, inspection bundle contracts, structural FEA, and examples.

## Non-Negotiable Gates

- Build the physical artifact, not a teaching diagram: no labels, callouts, cutaways, or explanatory slabs unless explicitly requested.
- Build real structure, not a silhouette: every required function needs actual
  geometry, interfaces, clearances, and validation evidence.
- Do not treat every model as printable; choose the process stack from load path, use, scale, and operating story.
- Use the component model for assemblies: parts build at origin, connectors position them, and data flows through the parent.
- Prove mechanisms with motion skeletons and pose checks before attaching final geometry.
- Use `verify.*` for dimensions, clearances, connector mates, collisions, and acceptance checks.
- Expected final collision count is zero unless an exact intentional overlap is declared and verified.
- Treat every failed run, render, inspect, required simulation, requested/process-critical export, or manual review finding as an iteration input. Fix the model or revise the design, then gather the same evidence again.

# Stage 4: Feedback And Iteration

Goal: make evidence gathering the middle of the build, not the final checkbox.

## Sub-Workflow

1. Integrate proven leaf modules upward into composed modules and then `main.forge.js`.
2. Gather automatic evidence at the smallest useful level: run, render, inspect, simulation, FEA, requested or process-dependent export smoke tests, and scripted checks.
3. Gather manual feedback where automation cannot judge the design: read every render, inspect product intent, compare against PR/FAQ, and check whether operation feels like the user's expected workflow.
4. For mechanisms, prove rest, mid-travel, limits, coupled states, mirrored states, contacts, stops, clearances, and controls before polishing geometry.
5. For simulation-ready work, read `simulation-feedback.md`, export MJCF or FEA packages, run the verifier or FEA workflow, inspect numeric/visual evidence, and iterate.
6. Convert every finding into exactly one of: model edit, design-doc revision, new evidence command, explicit residual risk, or user question.
7. Record iteration learnings in `NOTES.md`, especially API surprises, repeated workarounds, and places where a ForgeCAD primitive or doc would have prevented parameter hacking.
8. Repeat the same evidence after each fix. Do not call the model ready because a different, easier check passed.

## Acceptance Criteria

- `main.forge.js` runs and composes high-level modules through real interfaces.
- Targeted inspection evidence has been run and read for fit, hidden internals, components, collisions, walls, or surface risks.
- Required simulation and FEA behavior has been tested at module or system level before final packaging; export behavior has been tested only when the user requested export deliverables or the process depends on external files.
- Findings have been converted into edits or documented residual risks, then rechecked.
- The project docs show the design -> feedback -> iteration history clearly enough for the next agent to continue.
- `NOTES.md` captures learnings, API friction, non-obvious choices, and follow-up ideas clearly enough for a future product/API pass.
- The model behaves the way the user expects under the relevant poses, loads, contacts, or usage scenarios, or the gap is explicitly named.

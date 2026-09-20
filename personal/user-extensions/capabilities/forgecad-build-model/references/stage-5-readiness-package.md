# Stage 5: Readiness Package

Goal: package only after the feedback loop says the model is ready or the remaining validation loop is explicit.

## Sub-Workflow

1. Run the final entry point after the last edit.
2. State the intended physical component graph: one connected component, intentionally separate purchased parts, selected assembly plus ghosts, or another exact structure.
3. Rerun the decisive evidence from Stage 4: inspection bundles, simulation/FEA checks, motion poses, manual render views, and requested or process-dependent exports.
4. Read `readiness-review.md` and fill the requirement checklist with pass/partial/fail/unknown evidence.
5. Verify BOM entries and builder-critical `dim()` annotations are present.
6. Run exports only when the user requested deliverable files or the chosen output standard depends on external process files. Otherwise, record that exports were not requested and do not create them just to finish the build. When exports are in scope, run the process-appropriate commands or name license/tool-gated commands that complete the package:
   - printed parts: STL or 3MF
   - machined/CAD interchange: STEP
   - sheet goods: flat pattern or cutting layout
   - simulation: MJCF plus MuJoCo evidence
   - structural study: FEA export plus solver/report evidence
7. Read every generated PNG, manifest, report, simulation result, or in-scope export failure. Treat failures as iteration inputs unless time or tooling blocks them.
8. Clean up transient inspection/render/simulation output directories created inside the model folder, especially default `outputs/` bundles. Keep only user-requested deliverables, in-scope process exports, or curated evidence intentionally referenced by the docs.
9. Review `NOTES.md` and make sure it captures the useful learnings, API frustrations, non-obvious modeling decisions, cleanup notes, and follow-up ideas from the build.
10. Deliver an evidence-backed readiness summary: what passed, what remains unverified, and what validation loop comes next.

## Acceptance Criteria

- The final file or `main.forge.js` runs.
- Component count matches the intended physical component graph.
- Collision evidence reports zero unexpected findings.
- Critical mechanical interfaces are proven with `verify.*` and inspection evidence.
- Moving assemblies have pose and behavior evidence across their operating range.
- Required simulation/FEA evidence is present or explicitly blocked; export evidence is present only when requested or process-critical.
- Requirement checklist is evidence-backed and unknowns are named.
- Transient `outputs/` clutter has been removed or explicitly kept for a reason.
- `NOTES.md` is present for non-trivial work and captures useful build learnings or says there were none.
- The final response names commands run, retained evidence paths if any, views checked, component count, collision count, simulation/FEA results, requested export results if any, residual warnings, cleanup performed, notes captured, and intentional exceptions.

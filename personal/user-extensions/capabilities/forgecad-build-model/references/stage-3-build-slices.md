# Stage 3: Build Slices

Goal: build the model in small runnable increments and gather local evidence after each increment.

## Sub-Workflow

1. Implement one slice at a time: profile, sketch, path, mechanism rig, imported purchased-part wrapper, leaf module, or composed module.
2. Keep slices local. Do not hide final assembly placement inside a part file.
3. Add builder props, preview-only params, user-facing parent params, connectors, returned metadata, `dim()`, BOM entries, and `verify.*` checks as soon as they become part of the contract.
4. Run the slice with the local CLI:

   ```bash
   node dist-cli/forgecad.js run path/to/file.forge.js
   ```

5. Render or inspect the smallest evidence view that can falsify the slice. Read `inspection-feedback.md` for fit, wall, component, section, and identity evidence.
6. If evidence fails, edit the model or update the design doc, then rerun the same check.
7. Append commands, findings, design changes, and retained evidence paths to the relevant module doc. Do not keep transient inspection bundles just to document that a check ran.
8. Append build learnings to `NOTES.md`: what was not obvious, API friction, helper/primitive gaps, inspection surprises, cleanup performed, and follow-up ideas.

## Acceptance Criteria

- Every added module runs standalone where practical.
- Every structural part exposes connectors or metadata needed by its parent.
- Siblings do not import each other; the parent routes data and parameters.
- Good params are present for user-adjustable design decisions, with safe defaults, ranges, units, integer/choice/list/manual types where appropriate, and verification for dangerous extremes.
- No named part contains unintentional disconnected matter.
- Fasteners, cables, covers, handles, panels, and purchased parts have receiving geometry and a load path.
- Each slice has enough render/inspect/manual evidence to justify moving to the next slice.
- `NOTES.md` captures non-obvious learnings or explicitly says there were none.

## Rejection Signals

- A screw head without a receiving hole, boss, insert, nut, or through-stack.
- A handle, cable, rail, or panel touching by tangent contact only.
- A structural part positioned by final `translate()` instead of a connector or parent-level interface.
- A user-facing `param()` that is just an unexplained magic number, or a critical design choice hidden as an uneditable constant.
- `console.log()` used as validation where `verify.*` should encode the contract.
- A repeated workaround, magic number, or manual trigonometry pattern that should be a ForgeCAD primitive, helper, or clearer submodule.

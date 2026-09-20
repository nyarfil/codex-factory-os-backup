# Stage 2: Architecture Plan

Goal: define the model architecture, docs, interfaces, and evidence gates before full implementation.

## Sub-Workflow

1. Write `docs/HLD.md` for the high-level design: system concept, component graph, major interfaces, materials/processes, assembly story, and failure modes.
2. Add `docs/LLD-*.md` or `docs/modules/*.md` only where the project needs lower-level decisions: complex parts, mechanisms, electronics packages, FEA regions, imported parts, simulation contracts, or manufacturing details.
3. Plan the file tree as one nested `modules/` tree: leaf modules, composed modules, system-level `main.forge.js`. The central file should compose high-level concepts, not import every leaf.
4. Read `module-contracts.md` and define the module contract: reusable files return builder functions, direct-run previews live under `if (require.main === module)`, parts build locally at origin, parent modules position children, and data flows down through props and up through returned metadata.
5. Read `parameter-controls.md` and plan user-facing params: which values belong in the parent, which are preview-only, which stay derived, and which need choices, lists, manual sheets, anchors, or range checks.
6. Define implementation order: start with profiles, constrained sketches, path/rig skeletons, imported purchased-part wrappers, or the smallest submodule that can gather useful feedback.
7. Define evidence gates per module: run, render views, section/fit/thickness/components inspection, motion poses, simulation, FEA, requested or process-dependent exports, and manual review questions.

## Acceptance Criteria

- HLD exists and matches the product intent.
- Needed LLD/module docs exist; unnecessary docs are not created.
- `main.forge.js` is planned as the central entry point.
- The nested file structure keeps files small and composes upward through modules.
- User-facing params have names, defaults, units/ranges, ownership, and validation intent; non-user-facing dimensions remain derived from design intent.
- Every important dimension, interface, and motion range has a reason or a provisional assumption.
- The first 1-3 implementation slices and their feedback checks are named.

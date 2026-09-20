# Inspection Feedback

Use `forgecad inspect ...` when a shaded render is too ambiguous and you need structured evidence: collision bundles, sections, wall thickness, physical components, masks, depth, normals, surface continuity, fit, or comparison overlays. Inspection is feedback for the design loop; unexpected findings are model bugs or design gaps to fix and reinspect.

## Workflow

1. Identify the failure question: overlap, thin walls, hidden cavity failure, disconnected or fused bodies, floating parts, wrong identity, orientation artifacts, or surface continuity.
2. Confirm the model executes. In this repo use `node dist-cli/forgecad.js run model.forge.js`; use `--debug-imports` for suspect imports.
3. Pick one targeted evidence command. Use `forgecad inspect evidence` and the core `forgecad` skill's CLI docs for exact syntax. For exploratory checks, pass `--output /tmp/forgecad-inspect-<slug>` when supported so default `outputs/inspect` bundles do not clutter the model folder.
4. Summarize the manifest first, then use `jq` for targeted follow-up:

   ```bash
   python <forgecad-build-model-skill-dir>/scripts/summarize_manifest.py /tmp/model-inspect
   ```

5. Inspect the PNGs, not only JSON. Read identity/context images first, then risk evidence, then orthogonal cameras or sections when iso hides the issue.
6. Isolate intentional overlaps with `--focus "A,B"` or `--hide "C"` so the remaining report stays meaningful.
7. Convert findings into edits, design-doc changes, or explicit residual risks, then rerun the same command.
8. After findings are summarized and no bundle needs to be preserved, delete transient inspection output directories created inside the model/project folder. Keep only user-requested deliverables or explicitly curated evidence.

## Evidence Selection

| Question | Evidence command |
|----------|------------------|
| Quick visual sanity | `inspect visual image` |
| Kinematic rig, joints, axes, and links | `inspect visual rig` |
| Object naming and identity | `inspect visual objects` |
| Exact local section measurement, bore widths, rib thickness through a chosen line | `inspect section --ray ...` |
| Hidden internals, cavities, pockets, screw paths, captured components | `inspect sections at\|stack\|sample` |
| Multi-part interference, fit checks, ghost parts, moving clearances | `inspect fit interference` |
| Printability, shell walls, ribs, bosses, snaps, slots | `inspect manufacture thickness` plus sections |
| Parts without a mesh-contact path to the ground | `inspect physical floating` |
| Accidental fusion, connected solids | `inspect physical components` |
| Air gaps between physical components | `inspect physical gaps` |
| Surface orientation, occlusion, faceting, strange protrusions | `inspect visual depth` or `inspect visual normals` |
| Loft, fillet, skin, and sweep surface continuity | `inspect surface zebra` or `inspect visual normals` |
| Reference-vs-candidate reconstruction comparison | `inspect compare overlay --with reference.3mf` |

## Section Probe And Replay

```bash
node dist-cli/forgecad.js inspect section model.forge.js --plane yz --ray bore:-20,0:20,0 --output /tmp/forgecad-inspect-bore
node dist-cli/forgecad.js inspect replay /tmp/forgecad-inspect-bore/result.json --source candidate.forge.js
```

The probe contract lives in the core `forgecad` skill's inspection-bundles guide.

## Misread Traps

- Face-touching is not a collision; collision findings are positive-volume overlaps.
- Gray/unresolved thickness area means evidence is incomplete, not safe.
- Distance/gap figures are bbox-gap metrics between components, not closest-surface distances.
- Depth, normals, and zebra are visual aids, not exact measurements or curvature proofs.
- Resolve mask colors through the manifest's object list, never by object order.

## Reporting

Record exact command, manifest highlights, PNG views inspected, findings, and the model/design edit made from those findings. Record bundle paths only for retained evidence; otherwise state that transient inspection outputs were removed. Never claim geometry is verified if only `forgecad run` passed.

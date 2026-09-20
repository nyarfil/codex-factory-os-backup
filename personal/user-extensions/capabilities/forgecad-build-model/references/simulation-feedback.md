# Simulation And FEA Feedback

Use this when dynamic behavior, contacts, controls, joint travel, load paths, or structural stress affect readiness. Successful export is not readiness; the exported package must be exercised and the evidence must feed back into design changes.

## MuJoCo Workflow

1. Export from the exact source file:

   ```bash
   rm -rf /tmp/forgecad-mjcf && mkdir -p /tmp/forgecad-mjcf
   node dist-cli/forgecad.js export mjcf path/to/model.forge.js --output /tmp/forgecad-mjcf
   ```

2. Load `scene.xml`, not only a model XML, so floor/camera/package context is included.
3. Check root behavior. Free-root models need real support/contact geometry or an explicit fixed-root export path.
4. Check initial poses numerically; visual intuition can disagree with joint refs and connector frames.
5. Keep meaningful collisions. Do not disable functional contacts just to make motion pass; use defensible simplified colliders when mesh contact is unstable.
6. Define numeric acceptance before the run: expected signed travel, final velocity, stopping behavior, root drift, contact pairs, or drive cycles.
7. Render initial, settled, and driven frames from views that show the moving parts and contact interfaces.
8. Interpret contacts and motion; if the mechanism jitters, moves the wrong direction, overshoots, jams, falls through the floor, or contacts impossible proxy geometry, edit the model and rerun.

Helper script:

```bash
uv run --python 3.11 --with mujoco --with pillow \
  python <forgecad-build-model-skill-dir>/scripts/mujoco_verify.py /tmp/forgecad-mjcf \
  --settle-seconds 2 \
  --seconds 8 \
  --actuator drum_velocity=-0.75 \
  --watch-joint drum_joint \
  --expect-drive-cycles drum_joint=-0.06:-0.03 \
  --expect-final-qvel drum_joint=-0.02:0.02 \
  --render-dir /tmp/forgecad-mjcf/verify \
  --camera-preview-grid
```

Use `--actuator name=value` more than once for multi-actuator models. Use `--expect-drive-cycles joint=min:max` for revolute travel in cycles, `--expect-drive-delta joint=min:max` for raw MuJoCo qpos units, and `--expect-final-qvel joint=min:max` for terminal velocity.

## FEA Workflow

1. Use the core `forgecad` skill's structural FEA guide and generated assembly docs for `Fea.*`, `withFeaStudy(...)`, export syntax, materials, fixtures, loads, regions, and solver limits.
2. Define the load case before export: what is fixed, what is loaded, what material is assumed, and what stress/displacement result decides readiness.
3. Mark only bodies and regions that have real structural meaning. Do not invent fixtures, loads, or materials to make a report pass.
4. Run the FEA workflow through the cloud provider when available:

   ```bash
   forgecad fea run path/to/model.forge.js --provider daytona
   ```

   Use `--provider local` only for package-debugging environments that intentionally have local solver tools installed.
5. Inspect deformation, stress concentration, reaction sanity, and mesh warnings.
6. If results violate expectations, edit geometry, material, support, load path, or design intent, then rerun the same study.

## Reporting

Record export commands, verifier commands, numeric results, contact pairs, rendered frames, FEA report paths, solver warnings, and the design/model iteration they caused. Say what was not verified. Never claim simulation or build readiness when only `forgecad run`, `check simready`, or a successful export was executed.

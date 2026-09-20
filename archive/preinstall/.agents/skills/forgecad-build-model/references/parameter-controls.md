# Parameter Controls

Use this when deciding which dimensions or design choices should become user-facing ForgeCAD parameters. The core `forgecad` skill remains the source of truth for exact `Param.*`, `param()`, manual parameter, CLI override, and anchor syntax.

## Good Parameter Rules

- Expose design decisions the user is likely to adjust: overall envelope, fit-critical clearances, material thickness, purchased-part model, pattern counts, named layout choices, mechanism positions, and presentation/cutaway states.
- Do not expose every intermediate number. Derived offsets, trig results, fillet compensation, connector locations, and sibling-placement math should be computed from intentful parent values.
- Put cross-cutting parameters in `main.forge.js` or the parent assembly, then pass ordinary props into child builders. Child modules may define preview-only params only under `if (require.main === module)`.
- Use names that are stable CLI keys and readable UI labels: `Wall Thickness`, `Servo Model`, `Door Open Angle`, not `w`, `x2`, or `tweak`.
- Provide defensible defaults, `unit`, `min`, `max`, `step`, and `integer: true` where relevant. Ranges should cover plausible use without allowing physically impossible geometry.
- Prefer `Param.choice()` for named options, `Param.bool()` for real toggles, `Param.list()` for repeated structured items, and manual sheets (`path2d`, `spline2d`, `placement2d`) when dragging geometry is the natural editing action.
- Add spatial anchors for parameters the user should edit from the model, especially manual sheets and fit-critical dimensions.
- Add `verify.*` checks for parameter extremes that can break geometry, clearances, connector mates, collision assumptions, or requested export readiness.

## Rejection Signals

- A slider exists only because a magic number was not understood.
- A child module owns a parameter that changes sibling fit or assembly-level layout.
- A parameter range permits zero wall thickness, negative clearances, invalid counts, impossible angles, or unsupported purchased-part combinations.
- Two parameters can contradict each other without validation.
- The final model is parametric in code but not meaningfully adjustable by the user.

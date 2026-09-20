# Stage 1: Design Intent

Goal: turn the request into a clear design target and first feedback plan before modeling.

## Sub-Workflow

1. Normalize the artifact: what it is, who uses it, where it lives, what it touches, how it is assembled, how it can fail, and what "ready" means.
2. Write `docs/PRFAQ.md` or an equivalent short design-intent doc for non-trivial work. Capture the user-facing promise, FAQ-style decisions, rejected obvious alternatives, and open questions.
3. Create or update `NOTES.md` in the model folder for live build notes: learnings, API friction, non-obvious choices, inspection surprises, and follow-up product/API ideas.
4. Choose the output standard. Default to a real product model. If the brief
   uses ambiguous wording such as "prototype", state the actual readiness level
   instead of guessing: visual-only concept, simulation-only asset, printable
   draft, validated physical prototype, or production-ready manufacturing
   package.
5. Choose the manufacturing/process posture from load path, scale, safety, quantity, environment, and operating story. Do not default to printing.
6. Define first-pass success criteria and feedback signals: renders, inspections, motion poses, FEA, MuJoCo, requested or process-dependent export checks, manual design review, or physical-world follow-up.
7. Ask the user for more requirements when the missing answer changes architecture, safety, manufacturing process, mating geometry, or readiness criteria. Prefer 1-3 concise questions with good options and their tradeoffs. If the options are low-risk, choose a defensible assumption, write it down, and proceed.

## Acceptance Criteria

- `docs/PRFAQ.md` or a compact equivalent exists for non-trivial work.
- `NOTES.md` exists for non-trivial work and is ready to collect build learnings and API friction.
- Output standard, process posture, assumptions, and purchased-part boundaries are explicit.
- The first feedback plan says what evidence will prove or falsify the design.
- Open questions are resolved through user answers, written as safe assumptions, or identified as true blockers with the options that would unblock them.

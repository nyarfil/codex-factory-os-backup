# Readiness Review

Use this in Stage 5 before reporting the model ready.

## Requirement Checklist

Extract the user request, PR/FAQ, HLD, LLDs, and module docs into must-haves and nice-to-haves. Mark every item:

| Result | Meaning |
| --- | --- |
| Pass | Evidence directly proves the requirement. |
| Partial | The requirement is present but incomplete or weakly evidenced. |
| Fail | The requirement is absent or contradicted by evidence. |
| Unknown | The current evidence cannot verify it. |

Unknowns count against readiness. Do not turn unknowns into passes because the model looks plausible.

## Evidence Caps

Use these as readiness gates, not as a standalone public grading skill:

- Model does not execute: not ready.
- Executes but cannot be rendered: not ready.
- No rendered images visually inspected: not ready.
- Only one flattering view inspected: not ready for real product delivery.
- Only the blurry outer silhouette matches the prompt: not ready. Zoom, section,
  inspect, and verify the function-bearing details.
- A must-have requirement is absent: say what is missing and what blocks readiness.
- Visually recognizable but physically impossible for the requested use: say what physical requirement fails.
- Ambiguous wording such as "prototype" does not waive physical reality checks;
  readiness depends on the stated validation scope.
- Internals, fit, walls, assembly behavior, or motion central to the brief but uninspected: say what still needs inspection.
- Multi-part assembly violates the component model: say which interface or ownership rule is broken.
- Inspection finds unexpected collisions, floating bodies, critical thin walls, or wrong connectivity: report the finding and required fix.
- Default flat lighting, material-false coloring, or teaching-diagram styling caps the presentation until fixed.

## Report Shape

The final response should include:

- requirement checklist summary
- evidence reviewed: run outcome, views inspected, inspection highlights, simulation/FEA results, and requested export results if any
- decisive strengths and remaining defects
- readiness summary: what is proven, what remains unverified, and what next validation loop is needed
- next fixes: the 2-5 highest-leverage improvements when not build-ready

Do not return a numeric score or fixed verdict label unless the user explicitly asks for one. The normal build workflow needs evidence, not grading theater.

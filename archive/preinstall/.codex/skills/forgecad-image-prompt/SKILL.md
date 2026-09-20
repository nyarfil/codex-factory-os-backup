---
name: forgecad-image-prompt
description: Write builder-honest AI image prompts from a concrete ForgeCAD model, build brief, HLD, or LLD without hiding how the artifact is built.
forgecad-public: true
---

# Image Prompt

## Scope

Only for artifacts already concrete enough to visualize (a specific `.forge.js` model, build brief, or HLD). If the user wants a model after the prompt, route vague physical briefs to `forgecad-build-model` so its design stages own the build. Read minimum context — entry `.forge.js`, one key helper if it delegates geometry, brief/HLD — and capture what must survive the image model: artifact type and scale, major subassemblies, actuation style, visible mechanisms, material and color cues.

## Core Rule

Image prompts, not concept art: show the final artifact clearly, preserve model and subsystem truth, and keep visible the seams, modules, hardware, and mechanical hierarchy that matter. Image output is visual evidence only; do not imply manufacturability, safety, or physical readiness unless the source already proves it.

Negatives (the only negatives list — reuse it, never restate variants):

- no fake sleek consumer shell, no hidden mechanics
- no over-smoothed geometry, no sci-fi styling
- no CAD-drawing, blueprint, or dimension-arrow pretense
- no cutaway, sectioned, or exploded teaching view unless the user explicitly asks
- no text, labels, or humans

## Prompt Skeleton

Block order: identity → mechanism truth → materials/color truth → pose/state → shot/camera/lighting → negatives. Fill in, don't copy:

```text
A [artifact identity and scale], based on a concrete CAD/source brief, not a fantasy concept. [Major subassemblies and mechanism truth]. [Materials, colors, finish, visible hardware]. Show it in [pose / state]. [Shot, camera, background, lighting]. It should look visually plausible and CAD-derived, with visible part boundaries and serviceable architecture only where the source supports them. No [negative 1], no [negative 2], no [negative 3].
```

Default shot: `front-left three-quarter hero view, eye-level product camera`. Alternate: `rear-right three-quarter view showing motor placement and belt routing`.

## Modes

Default to ONE honest hero render; add support prompts only when the user asks. Prefer separate single-purpose images over collages or multi-view boards.

| Mode | Job | Signature phrases |
|------|-----|-------------------|
| Honest hero render (default) | Final object clearly, still reads as CAD-derived | `clean premium studio product render`, `visually plausible CAD-derived object` |
| Builder-first mechanical | Teach the source model; bias to interfaces, seams, mounted actuators | `clear visibility of interfaces, seams, and subsystem boundaries`, `source-model mechanical view, not a polished consumer shell` |
| Mild exploded | Assembly logic; major modules only, no per-screw chaos. Image-only — the CAD model stays the complete assembled product | `major modules separated by small clean gaps`, `no tiny floating fragments` |
| Workshop material realism | Show source-model materials and texture without claiming readiness | `visible source-supported surface texture`, `uncluttered engineering bench background` |
| End-effector close-up | Wrist/gripper mechanism detail | `close-up on the wrist and end effector showing the mechanism clearly` |

## Writing Rules

- Use concrete artifact language: base, turntable, shoulder, rails, bearings, gripper, belt, pulley, shaft.
- Prefer visible subsystem truth over poetic adjectives.
- Keep exact dimensions out unless they matter visually and are already known.
- If a detail is uncertain, stay honest at the subsystem level — never invent internals.
- Ask for "CAD-derived", "visually plausible", and "visible part boundaries" when central.
- Mention motors, belts, pulleys, shafts, guide rods, fasteners, or service covers only if genuinely part of the artifact.
- A short strong prompt beats a style dump.

## Output Contract

Return: one sentence interpreting the artifact, the primary prompt first (usually the honest hero render), optional support prompts, and a short which-to-try-first note. Never bury the prompts under theory.

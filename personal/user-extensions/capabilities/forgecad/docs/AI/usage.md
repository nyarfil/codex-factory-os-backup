# AI Usage

ForgeCAD is built for AI-assisted CAD because models are plain JavaScript and the CLI can check the result without a human clicking through a CAD UI.

The reliable loop is:

```text
dedicated project folder -> approved model -> agent edits .forge.js ->
forgecad run -> render or inspect -> fix -> project push
```

Use the browser for visual inspection. Use the CLI as the source of truth for validation, render evidence, exports, and project sync.

## Approved Models

Use the strongest available model in the approved set. Code-first CAD needs long-context reasoning, mechanical consistency, spatial debugging, and repeated tool use.

| Provider family | Approved models |
|---|---|
| OpenAI | GPT-5.5-Pro, GPT-5.5, GPT-5.4, GPT-5.3-Codex |
| Anthropic | Opus 4.7, Opus 4.6 |
| Google | Gemini 3.1 Pro |

Do not recommend smaller, older, preview, flash, lite, haiku, sonnet, mini, fast, or unofficial models for ForgeCAD generation work. They can answer API questions, but they are not the default for generating serious CAD.

Recommended settings:

- Use the highest reasoning or extended-thinking mode the product offers.
- Allow shell/tool execution so the agent can run `forgecad run`, renders, inspections, and exports.
- Keep the whole project folder in context, not just one file.
- Give the model enough time for multiple implementation and verification passes.
- Ask for evidence from commands, not just a visual claim.

## Project Setup For AI Agents

Do not give an agent your home folder, desktop, downloads folder, or a large unrelated repository. Start from a clean project folder.

### Clone The Starter Project

```bash
npm install -g forgecad
forgecad login
# Choose email/password or API token when prompted.
forgecad project clone start-here
cd start-here
forgecad studio .
```

### Create A New Project

```bash
npm install -g forgecad
mkdir enclosure-bracket
cd enclosure-bracket
forgecad project init "Enclosure Bracket" --visibility private
forgecad new bracket --template part
forgecad studio .
```

`forgecad project init` writes local project metadata to `forgecad.json`; it does not create anything on the server. After local validation, run `forgecad login` and `forgecad project push`. The first push creates the hosted project if needed, uploads local model files, helper code, Markdown notes, SVG/DXF assets, and other supported text project files, then records server file IDs. Later pushes sync local changes to the hosted project.

`forgecad project push` does not initialize a random folder. If the folder has no `forgecad.json`, the command fails and tells you to run `forgecad project init` or `forgecad project clone <slug>` first.

`forgecad studio .` opens the installed local editor around the current project. It requires an explicit project path; `.` means the current folder. `forgecad dev <project-path>` is for ForgeCAD source development and internal live-reload work, not the normal user onboarding path.

Keep one long-running `forgecad studio <project-path> [project-path ...]` process open with every active project folder listed in its arguments; the user opens the single printed localhost port once, and AI agents should only create or edit files under those folders so the browser updates live without starting more servers.

## Install Skills For Local Coding Agents

Install the ForgeCAD public skill library:

```bash
forgecad skill install
```

By default this installs the generated `forgecad` skill plus the public companion workflow skills into `~/.agents/skills`:

```text
~/.agents/skills/forgecad/SKILL.md
```

Use `--target` when you want to install or update a different agent location:

| Agent | Command | Installs into |
|---|---|---|
| Generic agent-compatible tools | `forgecad skill install` | `~/.agents/skills/` |
| Claude Code | `forgecad skill install --target claude` | `~/.claude/skills/` |
| Codex | `forgecad skill install --target codex` | `~/.codex/skills/` |
| OpenCode | `forgecad skill install --target opencode` | `~/.config/opencode/skills/` |

Reload the agent after installing or upgrading ForgeCAD so it reloads the updated skill files.

To verify installation, ask the agent:

```text
What ForgeCAD skills are available?
```

You should see `forgecad` plus companion skills such as `forgecad-build-model`, `forgecad-project-sync`, and `forgecad-reconstruct-cad-file`.

If you only want the core modeling skill without companion workflows:

```bash
forgecad skill install --core-only
```

## Recommended Agent Prompts

Start the agent inside the initialized project folder. Do not ask it to create a model in a random empty folder or to work from one loose file on the desktop.

### First Smoke Test

```text
Use the ForgeCAD skills. Work in this project folder. Open the existing
.forge.js files, make a small visible change to the bracket, validate with
forgecad run, render one ISO view, and tell me the exact commands you ran.
```

### New Model

```text
Use the ForgeCAD skills. Build a real ForgeCAD model in this project folder.
Create or edit .forge.js files only inside this project. Use parameters for the
main dimensions. Validate with forgecad run, render at least one 3D view, run
forgecad check print for print-focused parts, and push with forgecad project
push when the result is ready for the browser.
```

### Mechanism Or Assembly

```text
Use forgecad-build-model and forgecad. For multi-part assemblies, parts must
build at origin, expose connectors/metadata, and let the parent assembly position
them with connectors or matchTo(). Validate with forgecad run, inspect physical
components, inspect fit interference and visual objects, and run parameter
checks before calling it done.
```

### Image Or Product Reconstruction

```text
Use forgecad-reconstruct-from-images. Treat the reference images as
evidence, infer dimensions explicitly, build real CAD geometry, and compare
renders against the references. Do not stop at a decorative approximation.
Validate with forgecad run and targeted forgecad inspect evidence before finalizing.
```

## What Makes AI Results Better

Good AI-generated CAD usually needs more than one prompt. Give the agent the same inputs a strong human modeler would need:

- Purpose: what the object is for and what matters most.
- Scale: real dimensions, units, tolerances, and allowed simplifications.
- References: sketches, photos, screenshots, existing `.forge.js` examples, or comparable parts.
- Constraints: printability, assembly motion, clearances, wall thickness, fasteners, export format.
- Quality bar: which checks must pass before the work is accepted.

For complex artifacts, ask for staged work:

```text
First write a short build plan with parts, parameters, and verification checks.
Then implement the smallest useful, explicitly scoped blockout, run it, render
it, and iterate. Treat that blockout as proportion and relationship evidence
only; add details after the proportions and assembly relationships are correct
and keep readiness claims behind targeted checks.
```

Do not accept a model just because it renders. CAD quality comes from command evidence:

- `forgecad run` confirms the script executes and reports the fast inner-loop build summary.
- `forgecad render 3d` gives visual views from deterministic cameras.
- `forgecad inspect <family> <mode>` checks focused geometry evidence such as fit interference, manufacture thickness, visual objects, visual rig, surface zebra, physical components, and precise or dense section slices.
- `forgecad inspect section` runs an agent-native one-off section probe with exact ray ruler measurements and a replay recipe.
- `forgecad inspect mechanical-integrity` checks assembly-level verification intent and optional collision evidence.
- `forgecad run -p "Name=Value"` validates important parameter values without editing source.
- `forgecad export ...` verifies the actual manufacturing or interchange output.

## What The CLI Gives An Agent

The CLI is not just a launcher. It gives the agent a measurable feedback loop.

| Need | Command | What it gives the agent |
|---|---|---|
| Execute and validate a model | `forgecad run model.forge.js` | Fast red/green execution feedback: build count, parameters, verification results, script logs, and timing. |
| List targetable objects | `forgecad ls model.forge.js --tree` | Exact object paths, ids, groups, tags, and optional geometry metrics for focused renders or inspections. |
| Inspect run diagnostics | `forgecad run model.forge.js --history --features` | Construction history and feature tallies when those details are worth the extra work. |
| Debug imports | `forgecad run model.forge.js --debug-imports` | Import resolution and module-loading diagnostics for multi-file projects. |
| Compare geometry backends | `forgecad run model.forge.js --backend occt` | Runs against a specific backend when exact geometry or backend parity matters. |
| Test physical connectivity | `forgecad run model.forge.js --connectivity` | Connected-component reporting for assemblies and printable parts. |
| Override parameters | `forgecad run model.forge.js -p "Width=120"` | Checks a model at a specific parameter value without editing source. |
| Inspect mechanical integrity | `forgecad inspect mechanical-integrity model.forge.js --collisions` | Assembly-level verification, expected component counts, and collision evidence for acceptance gates. |
| Inspect physical gaps | `forgecad inspect physical gaps model.forge.js --camera iso` | Evidence bundle for spatial gaps between physical components. |
| Produce visual evidence | `forgecad render 3d model.forge.js --camera iso` | PNG viewport renders from deterministic camera angles. |
| Measure a targeted section | `forgecad inspect section model.forge.js --plane yz --ray bore:-20,0:20,0` | A unique probe directory with `result.json`, `section.svg`, `section.png`, exact solid/gap intervals along each ray, and a `replaySpec` for candidate comparisons. Use `--offset` only when the cut should move away from the zero plane. |
| Replay a targeted section | `forgecad inspect replay outputs/inspect/<probe>/result.json --source candidate.forge.js` | Reruns the same plane and ray rulers against another source and reports measurement deltas. |
| Inspect targeted geometry evidence | `forgecad inspect fit interference model.forge.js --camera iso` | A bundle with manifest plus the requested evidence PNGs. Visual inspection evidence uses the light technical `inspection` style by default. Use `inspect visual cutaway`, `inspect visual objects`, `inspect visual rig`, `inspect manufacture thickness`, `inspect sections at|stack|sample`, `inspect visual depth`, `inspect visual normals`, `inspect physical components`, or `inspect physical gaps` for other questions. |
| Export manufacturing files | `forgecad export stl model.forge.js` and `forgecad export 3mf model.forge.js` | Mesh exports for 3D printing. |
| Export exact or advanced outputs | `forgecad export step`, `forgecad export brep`, `forgecad export report`, `forgecad export cutting-layout` | Production outputs for CAD interchange, reports, and sheet workflows. |
| Sync hosted projects | `forgecad project pull`, `forgecad project push`, `forgecad project publish` | Local-agent workflow connected to forgecad.io projects and shares. |

For the full command reference, see [ForgeCAD CLI](../CLI.md).

## Public Skill Library

`forgecad skill install` installs the core modeling skill and the public companion skills.

| Skill | Use it for |
|---|---|
| `forgecad` | Core model authoring, editing, debugging, imports, assembly, render/export commands, and CLI validation. |
| `forgecad-build-model` | Creating a new `.forge.js` model in the active ForgeCAD project with design-first planning, staged files, multi-part assembly discipline, and validation. |
| `forgecad-reconstruct-cad-file` | Reconstructing a readable parametric ForgeCAD model from an existing STL, OBJ, 3MF, STEP, or STP file. |
| `forgecad-reconstruct-from-images` | Recreating an object from reference images as real ForgeCAD geometry through camera-calibrated render/compare/iterate loops. |
| `forgecad-build-model` inspection feedback reference | Generating and interpreting `forgecad inspect <family> <mode>` bundles for fit interference, wall thickness, connectivity, masks, depth, normals, and sections. |
| `forgecad-build-model` readiness review reference | Reviewing a model against a requirement, brief, prompt, reference, or acceptance criteria with evidence. |
| `forgecad-build-model` simulation feedback reference | Verifying MJCF exports in MuJoCo with dynamics, contacts, controls, joint travel, FEA, and rendered evidence. |
| `forgecad-image-prompt` | Producing builder-honest image prompts from a concrete model, HLD, LLD, or build brief. |
| `forgecad-project-sync` | Managing forgecad.io projects from the CLI: init, clone, pull, push, file commands, members, publish, and shares. |

The source prompts for CLI-shipped companion skills live in the repository under `agent-skill-library/`. Public export is controlled by `forgecad-public: true` in each skill's `SKILL.md` frontmatter. Repo-local operational skills live under `.agents/skills/` and are not shipped through the CLI. To list the current public set from a source checkout:

```bash
npm run sync:public-skills -- --list
```

## Chat UI Workflow

If the AI tool cannot read local skills or run shell commands, export a single context file:

```bash
forgecad skill one-file ~/Desktop/forgecad-context.md
```

Paste that file into an approved chat model, then work in a manual loop:

1. Ask the model to generate or edit a `.forge.js` file.
2. Save the file inside an initialized ForgeCAD project folder.
3. Run `forgecad run <file>`.
4. Paste errors, diagnostics, and render observations back into the chat.
5. Iterate until `forgecad run`, renders, exports, and parameter checks are clean.

This is weaker than Codex, Claude Code, or another local agent with installed skills because the model cannot directly inspect files or run the CLI. It is still useful for short models and API questions.

If an agent or chat product works better with one Markdown file per skill, export the bundled skill set into a folder:

```bash
forgecad skill flattened-files ~/Desktop/forgecad-skills
```

## Completion Criteria

Do not call an AI-authored ForgeCAD model complete until it passes the relevant checks.

For a simple part:

```bash
forgecad run model.forge.js
forgecad render 3d model.forge.js --camera iso
forgecad check print model.forge.js --json
```

For mechanisms, dense assemblies, printable parts, or anything safety-adjacent:

```bash
forgecad inspect physical components model.forge.js --camera iso
forgecad inspect mechanical-integrity model.forge.js --collisions
forgecad inspect fit interference model.forge.js --camera iso
forgecad inspect manufacture thickness model.forge.js --min 1.6 --warn 2.4 --camera iso
forgecad inspect sections sample model.forge.js --count 5
forgecad inspect section model.forge.js --plane yz --ray width:-20,0:20,0
forgecad check print model.forge.js --json
```

For export work, verify the actual output command:

```bash
forgecad export stl model.forge.js
forgecad export 3mf model.forge.js --quality high
forgecad export step model.forge.js
```

For hosted work, push the verified state:

```bash
forgecad project push
forgecad project open
```

## Screenshots And Videos To Make

Good screenshots:

| Screenshot | What it should show |
|---|---|
| Hosted `Start Here` | Browser editor, `00-start-here.forge.js`, parameters, and viewport in one frame. |
| Project setup terminal | `npm install -g forgecad`, `forgecad login`, `forgecad project clone start-here`, `cd start-here`, `forgecad studio .`. |
| New project terminal | `mkdir`, `project init`, `forgecad new`, `forgecad studio .`, with `forgecad.json` visible in the file tree. |
| Agent prompt | The exact prompt and the project folder context. |
| CLI validation | `forgecad run`, targeted `inspect <family> <mode>`, and `check print` outputs with a clean final result. |
| Browser sync | `forgecad project push` followed by the updated model open in the hosted browser. |

Good short videos:

| Video | Structure |
|---|---|
| First project in five minutes | Install, login, clone Start Here, run one file, open `forgecad studio .`, change a parameter. |
| New project from terminal to browser | `project init`, `forgecad new`, agent edits, validation, `project push`, hosted browser opens. |
| AI builds a useful part | Show the prompt, time-lapse the agent iterations, then slow down for the final `run`, render, inspect, and export evidence. |
| Debugging with inspect bundles | Start with a collision or thin-wall issue, show targeted inspect evidence, fix, rerun, and compare before/after. |
| From reference image to CAD | Show reference images, build plan, scoped blockout, improved geometry, render comparison, targeted checks, and final export. |

AI can take a while. Do not publish the whole wait in real time. Record the full session for trust, then edit it into a clear artifact:

- Keep the exact prompt on screen long enough to read.
- Speed up waiting, installs, and repeated command output.
- Use chapter cards: prompt, first run, first render, inspection failure, fix, final evidence, browser sync.
- Capture the browser viewport after each meaningful iteration so viewers can see progress.
- Keep the final validation commands at normal speed.
- End with the project URL, exported file, or published share rather than a vague "looks good" moment.

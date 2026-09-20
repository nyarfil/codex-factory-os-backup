# Phase 07 — Full re-read and repair review

Date: 2026-09-20

This review treats the files physically present in the workspace as the source of truth. Earlier conversational progress claims were not accepted as evidence.

## Material defects found and repaired

1. **Missing implementation files despite earlier PASS claims.** Phase 01 lacked `models.py`, `policy.py`, `cli.py`, and tests; Phase 04/05/06 also referenced absent modules. Reconstructed required modules and added fresh-process tests.
2. **Custom-agent artifacts were catalog-only.** The 31 native Codex TOML agent files were absent. Generated and validated all 31 files from the reviewed catalog.
3. **Two Factory skills were absent and reference files were missing.** Added Data and Document entry skills plus the referenced progressive-disclosure material for General/Software/CAD-3DP/Research.
4. **Hook output schema was wrong.** Replaced top-level `additionalContext` output with the documented `hookSpecificOutput.hookEventName` / `additionalContext` form. PreToolUse denial uses the documented permission-decision form.
5. **Governor CLI argument-order bug.** JSON/Markdown output helpers were called with reversed arguments. Corrected and added an end-to-end CLI test.
6. **Installer could accept an incomplete distribution.** Added source-bundle completeness validation before any mutation.
7. **Uninstall could delete locally modified Factory resources.** Agent/Skill fingerprints are now checked; modified or extra managed resources are preserved with warnings.
8. **Static Sol model ID was too rigid.** Logical Sol now prefers `gpt-5.6`, with `gpt-5.6-sol` treated as an alias by runtime resolution/audit. Actual availability remains governed by `model/list`.
9. **Astra quota policy was too aggressive.** Red quota now produces a strict economy warning rather than automatically blocking a hard problem. Exhausted/unavailable Astra can be denied/fallbacked.
10. **Per-turn hook context was too large.** UserPromptSubmit now injects a short routing cue; detailed factory guidance is loaded lazily from Skills.
11. **Subagent fan-out policy was too permissive.** Default guidance now uses no child for trivial tasks, normally 1–2, 3–4 only for large independent reads, and 5–6 only exceptionally.
12. **Stale documentation/test-count claims.** Final documentation is regenerated from the final workspace/test run rather than copied from earlier conversational claims.

## Deliberate non-features

- Factory OS does not claim a platform-level privilege above Codex/system/admin/security policy. It is the top-level **user-managed customization control plane**.
- It does not auto-delete existing MCPs, Rules, Skills, Agents, or Hooks. Governor inventories first; cleanup is reviewed and reversible.
- It does not infer a successful task from a subagent saying "done". Historical adaptive routing is withheld until verified outcomes can be recorded reliably.
- It does not silently rewrite the user's existing `config.toml`. A reviewed recommended snippet is provided instead.

## Remaining environment-dependent gates

These cannot be proven inside this Linux container:

- native Windows Codex CLI/IDE smoke test on the user's machine;
- the user's actual model availability/quota response;
- hook trust approval (`/hooks`) in the user's Codex UI/CLI;
- the actual contents of the user's existing MCP/Rule/Skill environment, which should be scanned after Factory OS installation.

The package therefore includes Doctor, model audit, Governor, backups, and safe uninstall rather than pretending these gates were already passed.

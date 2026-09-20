# Phase 3 Sources

Primary current Codex documentation consulted during this phase:

- OpenAI — Build skills: https://developers.openai.com/docs/build-skills
  - Skills use `SKILL.md` with required `name` and `description` metadata.
  - Codex first uses Skill metadata for discovery and loads the full Skill only when selected.
  - Skills may be implicitly selected from their descriptions.
  - Global skills live under `~/.agents/skills`; repository skills live under `.agents/skills`.
  - `agents/openai.yaml` may set `policy.allow_implicit_invocation`.

- OpenAI — Customization overview: https://developers.openai.com/docs/customization/overview
  - `AGENTS.md`, Skills, MCP, and subagents are complementary customization layers.

- OpenAI — Subagents: https://developers.openai.com/docs/agent-configuration/subagents
  - Applicable `AGENTS.md` or Skill instructions can request delegation.
  - Custom agents may override model/reasoning/sandbox settings.

- OpenAI — AGENTS.md: https://developers.openai.com/docs/agent-configuration/agents-md
  - Global and repository-level guidance are layered before work begins.

# Runtime compatibility notes

The current official Codex documentation supports user-level custom agents under `~/.codex/agents/`, with `name`, `description`, `developer_instructions`, and optional `model`, `model_reasoning_effort`, `sandbox_mode`, MCP, and skill settings.

This component deliberately does **not** assume that every installed Codex build will always honor role-level model overrides correctly. There have been public regression reports in some 5.6-era CLI builds where spawned custom roles inherited the parent model/effort. Later phases therefore must:

1. Probe the installed Codex version and active multi-agent backend.
2. Verify that requested role/model/effort appears in the spawned child metadata when possible.
3. Prefer native custom-role spawning when it works.
4. Fall back to explicit model/reasoning overrides plus the matching role instructions from `agent_catalog.json` when the runtime exposes model overrides but role selection is unreliable.
5. Fall back again to parent-model inheritance only when the requested model is unavailable, and report the downgrade.

Do not solve this by silently pretending a child is Astra/Terra when runtime metadata says otherwise.

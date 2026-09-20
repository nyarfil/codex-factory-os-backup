# Example cleanup plan

This is an example only. Phase 05 never applies these actions automatically.

1. Keep one Factory OS global control-plane guidance source.
2. Review project `AGENTS.md` files that contain model-routing or orchestration commands; retain repository constraints but remove control-plane takeover directives.
3. Merge duplicate skills that advertise the same logical capability.
4. Keep universal MCP servers global; move project-specific MCPs to project scope where practical.
5. Consolidate `hooks.json` and inline `[hooks]` in the same layer into one representation.
6. Replace broad shell `allow` rules with narrow command prefixes and validate them with `codex execpolicy check`.
7. Record a before/after ownership snapshot before any mutation in the later installer/cleanup phase.

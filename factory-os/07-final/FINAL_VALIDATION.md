# Final validation checklist

The final ZIP must not be produced until all items below pass in a fresh process.

- Python compileall succeeds.
- No missing relative imports.
- All 31 custom-agent TOMLs parse.
- Exactly six Factory entry Skills exist and local reference links resolve.
- Hooks output documented event-specific JSON.
- Router / Agent / Skill / Runtime / Governor contracts pass.
- Simulated existing Codex HOME survives install and uninstall with unrelated AGENTS/MCP/Skill/Agent/Hook state preserved.
- Incomplete source bundles fail before mutation.
- Locally modified Factory Agent/Skill resources survive uninstall.
- Cleanup defaults to dry-run and only supports reversible quarantine/restore.
- Governor scan is non-destructive.
- Root package contains Windows entrypoints and installation guide.
- ZIP checksum is generated after packaging.

## Final run result

- Phase 01: 9 tests
- Phase 02: 14 tests
- Phase 03: 5 tests
- Phase 04: 14 tests
- Phase 05: 16 tests
- Phase 06: 8 tests
- Phase 07 distribution: 4 tests
- **Total: 70/70 PASS**
- Python compileall: PASS
- Missing relative imports: 0
- JSON/TOML parse errors: 0
- Broken Skill references: 0

See `final-test-output.txt` for the captured final pytest run.

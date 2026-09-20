# Phase 2 Decisions

1. **Role specialization is separate from model routing.** The same domain can use multiple roles, while Phase 1 still decides the cost/performance tier.
2. **Astra is a specialist before it is a writer.** Every Astra role in this phase is read-only. Bulk edits remain with Sol/Terra.
3. **Single integration owner.** Parallel agents may investigate or edit independent modules, but final reconciliation is owned by one Sol integration agent.
4. **No MCP/skill pinning inside agent TOMLs.** Omitting those keys preserves inheritance from the parent and avoids breaking the user's existing mixed MCP/skill environment.
5. **TOML + JSON catalog.** TOMLs are the native Codex representation; the JSON catalog gives later phases a deterministic source for explicit spawn/model fallback when Codex runtime behavior varies by version.
6. **No dangerous full-access profiles.** Writers use `workspace-write`; researchers and reviewers use `read-only`.
7. **Domain knowledge lives in domain roles, not the global parent.** This keeps the main orchestration context smaller and lets future CAD/software skills evolve independently.

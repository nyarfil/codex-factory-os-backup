# Phase 05 design decisions

1. **Factory OS is the user-managed control plane.** MCP/Rules/Skills/Agents/Hooks/project guidance are managed resources, not peer orchestrators.
2. **Do not lie about native precedence.** Codex still applies its own instruction/config hierarchy. We achieve practical central governance by auditing subordinate resources and later installing Factory OS cues/hooks, not by claiming an impossible hard override.
3. **Scan-only first.** A first-installed governance layer must understand an existing messy environment before mutating it.
4. **No silent deletion.** Phase 05 can propose keep/merge/disable/quarantine dispositions but applies none of them.
5. **Rules are narrowly scoped.** Treat `.rules` as command execution policy, not a replacement for prompt instructions.
6. **MCP is capability, not authority.** A server may expose tools but may not own orchestration policy.
7. **Skills are workflows/knowledge.** Duplicate or globally sprawling skills are surfaced for consolidation, not automatically removed.
8. **Hooks are additive.** Because Codex may run multiple matching hooks, mixed/competing hook sources are inventoried and reconciled instead of assuming one hook can suppress another.
9. **Ownership must be explicit.** Every resource receives scope, ownership, hash, and metadata so future cleanup can be reversible and attributable.
10. **Security-sensitive findings are conservative.** Broad shell allow rules are critical findings; parsing failures are high severity.

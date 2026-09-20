# Factory OS Control Plane Contract

## Authority boundary

Factory OS is the top-level **user-managed Codex customization control plane** for this environment.

It owns:

- factory/domain selection;
- task decomposition and delegation policy;
- model and reasoning-effort routing;
- cost/quota posture;
- subagent fan-out limits and single-writer integration policy;
- cross-factory coordination;
- verification/escalation policy;
- lifecycle audit and environment governance.

MCP servers, Rules, Skills, Custom Agents, project guidance, and Hooks are managed resources beneath this control plane. They may provide local constraints, tools, workflows, specialist expertise, and lifecycle actions, but they must not independently redefine the global orchestration policy.

## Important implementation reality

Codex itself has native configuration and instruction precedence. Factory OS does not pretend it can override platform/admin/security policy or rewrite Codex's internal precedence rules.

Instead, the Environment Governor audits subordinate resources for meta-orchestration/model-routing directives and marks conflicting resources for reconciliation or quarantine. Project guidance is allowed to define repository-specific build/test/style/safety constraints; it is not allowed to silently become a second global orchestrator.

## Layer responsibilities

| Layer | Allowed responsibility | Not its job |
|---|---|---|
| Factory OS | routing, factories, models, delegation, integration, governance | domain implementation details |
| AGENTS.md | persistent project/local constraints | independent global model router |
| Skills | reusable workflow/domain expertise | global orchestration takeover |
| MCP | external capability/tool access | policy authority |
| Custom Agents | bounded specialist execution | self-expanding orchestration hierarchy |
| Hooks | lifecycle cues, audit, guardrails | sole enforcement mechanism |
| Rules | sandbox-external command policy | general prompt/instruction policy |

## Mutation rule

Phase 05 is scan-only. Existing resources are never deleted, disabled, renamed, or rewritten automatically. Cleanup becomes possible only in a later phase using backup-first reversible operations based on a reviewed governance report.

# Phase 4 Decisions

## 1. App Server is the source of truth for selectable models

Static model names age badly. Runtime availability is determined from `model/list`, including each model's advertised reasoning efforts.

## 2. Quota logic is intentionally conservative

`account/rateLimits/read` is useful for general usage posture, but an explicit model→rate-limit-bucket mapping is not guaranteed. Factory OS therefore does not hard-code opaque bucket IDs or claim that Terra/Luna/Astra use independent pools unless the runtime explicitly proves it.

## 3. Astra gating affects optional specialist escalation first

When quota is red, optional Astra specialists are suppressed. Normal Sol/Terra work is not aggressively rewritten solely from quota percentages because model-specific metering can evolve independently of this package.

## 4. Hooks activate and audit; Router decides

Hooks are not trusted as a perfect policy boundary. `UserPromptSubmit` injects the operating rules every turn; Phase 1 remains the deterministic route engine; `SubagentStart` audits the model Codex actually reports.

## 5. Runtime mismatch is fail-visible

If a custom agent profile says `gpt-6-astra` but the SubagentStart hook reports `gpt-5.6-sol`, Factory OS logs it and tells the child not to claim Astra execution. Silent model substitution is unacceptable for evaluation and cost accounting.

## 6. No blind spawn-agent input routing

Modern multi-agent execution may hide the child message from PreToolUse. The spawn hook therefore enforces generic scope/fan-out rules only. Task-sensitive child selection remains the parent's responsibility plus the Phase 1 route.

## 7. Probe is read-only and cached

The App Server probe performs initialize → model/list → account/rateLimits/read only. It never starts a thread/turn. Hooks cache the result to avoid launching an App Server process on every prompt.

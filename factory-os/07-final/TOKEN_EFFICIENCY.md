# Token / cost / latency policy

Factory OS is optimized for **successful work per paid token**, not minimum token count in isolation.

## Persistent context budget

Approximate static discovery surface in the reviewed build:

- global Factory OS AGENTS block: ~224 tokens;
- 31 custom-agent descriptions: ~624 tokens total if all descriptions are surfaced;
- six Factory skill descriptions: ~225 tokens total (approximate); full Skill bodies are progressive-disclosure and load only when selected;
- UserPromptSubmit routing cue: ~30 tokens per turn;
- custom-agent developer instructions: loaded only when the corresponding child is spawned, not all at once.

These are approximate whitespace-based estimates, not tokenizer billing measurements.

## Model policy

- **Luna:** very bounded extraction/repetition only.
- **Terra:** default bulk read work, repository mapping, routine implementation/testing where acceptance criteria are clear.
- **Sol:** normal senior ownership, integration, architecture, hard debugging, mechanical/CAD engineering.
- **Astra:** scarce read-only specialist for hard/novel/repeatedly failing reasoning. Return implementation to Sol/Terra unless a true rescue requires otherwise.

Concrete model IDs are treated as runtime capabilities; logical roles should survive future model renames.

## Delegation policy

Subagents consume additional tokens. Therefore:

- trivial task: zero children;
- normal non-trivial task: 1–2 bounded children when useful;
- large independent read/research task: 3–4;
- 5–6 only when clearly shortening the critical path;
- no duplicated search merely to create a vote;
- overlapping writes remain single-owner by default.

## Context policy

- keep logs, test output, geometry dumps, and source corpora in files/tools;
- return paths, measurements, decisions, failures, and concise evidence to the parent;
- use one Factory entry Skill per domain and lazy references instead of many always-visible specialist Skills;
- probe Codex App Server only at meaningful boundaries (not on every ordinary prompt);
- expensive Astra availability/quota probing occurs at the Astra spawn boundary.

## Verification economics

When deterministic validation is available, prefer a cheaper generator + strong validation over paying the strongest model for every attempt. Escalate after **verified failure**, not merely model uncertainty.

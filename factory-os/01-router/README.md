# Codex Factory OS — Phase 1: Deterministic Factory Router

This component is intentionally independent from Codex hooks, custom agents, MCPs, and Skills.
It converts a **Task Contract** into a deterministic **Route Decision**.

The LLM may describe the task, but it does not get to freely invent which expensive model to use.
The router makes that decision from explicit fields: domain, task type, complexity, uncertainty,
novelty, blast radius, failure history, verification strength, context size, and parallelizability.

## Design goals

1. Use the cheapest model tier that is likely to finish correctly.
2. Reserve Astra for genuinely difficult reasoning/rescue work.
3. Prefer Astra as a bounded **specialist/adviser** and return implementation to Sol/Terra where practical.
4. Do not parallelize overlapping writes.
5. Increase verification before increasing model cost when strong deterministic verification exists.
6. Keep routing explainable: every decision contains human-readable reasons.
7. Keep model IDs out of domain rules. Logical tiers map to concrete models in one place.

## Quick test

```bash
python -m unittest discover -s tests -v
```

## Example

```bash
python -m factory_router.cli --pretty <<'JSON'
{
  "domain": "software",
  "task_type": "implementation",
  "complexity": 3,
  "uncertainty": 2,
  "novelty": 1,
  "blast_radius": 2,
  "failure_count": 0,
  "verification_strength": 4,
  "parallelizability": 3,
  "write_overlap_risk": 2,
  "context_size": 3
}
JSON
```

## Output contract

The result contains:

- `factory`: selected specialist factory
- `primary`: model tier + reasoning effort for the lead/worker
- `specialist`: optional bounded specialist model (normally Astra)
- `implementation_handoff`: optional cheaper model after specialist analysis
- `parallelism`: safe worker count and read/write policy
- `verification`: minimum verification level
- `escalation_chain`: what to try next after verified failure
- `reasons`: explainable routing evidence

This phase deliberately does **not** modify `~/.codex`.

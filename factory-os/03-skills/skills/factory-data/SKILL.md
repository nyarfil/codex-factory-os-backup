---
name: factory-data
description: Data analysis factory for datasets, tables, metrics, validation, quantitative reasoning, and reproducible analysis. Use for structured-data work rather than general software coding.
---

# Data Factory

## Mission
Produce reproducible, inspectable analysis with the cheapest capable model and deterministic computation wherever possible.

1. Establish source, grain, schema, freshness, units, missingness, and join keys before analysis.
2. Use `data_analyst` for bounded extraction/analysis; use Sol-level parent reasoning for ambiguous metric definitions or decision synthesis.
3. Prefer code/queries for arithmetic and aggregation; never ask the model to estimate values that can be computed.
4. Separate observed values, transformations, assumptions, and conclusions.
5. Validate totals, duplicates, nulls, ranges, and key reconciliations before presenting a decision.
6. Keep large intermediate tables out of parent context; return concise statistics, paths, and verification evidence.

from __future__ import annotations

from .models import (
    BudgetMode, Domain, ModelAssignment, ModelTier, ParallelismPlan,
    ReasoningEffort, RouteDecision, TaskContract, VerificationPlan,
)
from .policy import MODEL_IDS, TIER_ORDER, baseline_for


def _tier_index(tier: ModelTier) -> int:
    return TIER_ORDER.index(tier)


def _bump_tier(tier: ModelTier, amount: int = 1) -> ModelTier:
    return TIER_ORDER[min(len(TIER_ORDER) - 1, _tier_index(tier) + max(0, amount))]


def _lower_tier(tier: ModelTier, amount: int = 1) -> ModelTier:
    return TIER_ORDER[max(0, _tier_index(tier) - max(0, amount))]


def _difficulty_score(t: TaskContract) -> int:
    # 0..~60. Complexity/uncertainty carry most weight; failure history is capped.
    score = (
        3 * t.complexity
        + 3 * t.uncertainty
        + 2 * t.novelty
        + 2 * t.blast_radius
        + 2 * min(t.failure_count, 4)
        + t.context_size
        + 2 * t.safety_criticality
    )
    # Strong deterministic verification reduces the intelligence requirement,
    # but never below the domain baseline by itself.
    if t.deterministic_tools_available and t.verification_strength >= 4:
        score -= 3
    return max(0, score)


def _choose_effort(base: ReasoningEffort, score: int, t: TaskContract) -> ReasoningEffort:
    if t.user_requires_max_quality or t.budget_mode == BudgetMode.MAX:
        return ReasoningEffort.XHIGH if score >= 30 else ReasoningEffort.HIGH
    if score >= 31:
        return ReasoningEffort.HIGH
    if score >= 20 and base == ReasoningEffort.MEDIUM:
        return ReasoningEffort.HIGH
    if score <= 8 and base == ReasoningEffort.HIGH:
        return ReasoningEffort.MEDIUM
    return base


def _apply_budget(tier: ModelTier, score: int, t: TaskContract, reasons: list[str]) -> ModelTier:
    if t.user_requires_max_quality:
        reasons.append("user explicitly requested maximum quality; do not economize routing")
        return _bump_tier(tier, 1) if score >= 22 else tier

    if t.budget_mode == BudgetMode.ECO:
        # Never force hard architecture/mechanism/debug work below Sol.
        floor = ModelTier.SOL if (
            t.task_type.value in {"architecture", "mechanism_design", "integration", "debug"}
            and score >= 20
        ) else ModelTier.LUNA
        candidate = _lower_tier(tier, 1)
        if _tier_index(candidate) >= _tier_index(floor):
            reasons.append("eco mode lowered the primary tier by one step")
            return candidate
    elif t.budget_mode == BudgetMode.QUALITY and score >= 18:
        reasons.append("quality mode raised the primary tier for a non-trivial task")
        return _bump_tier(tier, 1)
    elif t.budget_mode == BudgetMode.MAX:
        reasons.append("max mode permits strongest routing")
        return _bump_tier(tier, 1)
    return tier


def _assignment(tier: ModelTier, effort: ReasoningEffort, role: str, write_allowed: bool = True) -> ModelAssignment:
    return ModelAssignment(
        tier=tier,
        model_id=MODEL_IDS[tier],
        reasoning_effort=effort,
        role=role,
        write_allowed=write_allowed,
    )


def _parallelism(t: TaskContract) -> ParallelismPlan:
    # Parallel reads are cheap; writes are deliberately conservative.
    read_workers = max(1, min(6, t.parallelizability + 1))
    if t.write_overlap_risk >= 3:
        write_workers = 1
        strategy = "parallel-read-single-writer"
    elif t.parallelizability >= 4 and t.write_overlap_risk <= 1:
        write_workers = 3
        strategy = "parallel-independent-worktrees"
    elif t.parallelizability >= 3 and t.write_overlap_risk <= 2:
        write_workers = 2
        strategy = "parallel-independent-modules"
    else:
        write_workers = 1
        strategy = "single-writer"
    max_workers = max(read_workers, write_workers)
    return ParallelismPlan(max_workers, read_workers, write_workers, strategy)


def _verification(t: TaskContract, score: int, primary: ModelTier) -> VerificationPlan:
    high_risk = t.blast_radius >= 4 or t.safety_criticality >= 3 or score >= 30
    deterministic = t.deterministic_tools_available or t.verification_strength >= 4
    if high_risk:
        return VerificationPlan("strict", True, deterministic)
    if primary in {ModelTier.SOL, ModelTier.ASTRA} or score >= 18:
        return VerificationPlan("standard", True, deterministic)
    return VerificationPlan("light", False, deterministic)


def route_task(t: TaskContract) -> RouteDecision:
    reasons: list[str] = []
    base = baseline_for(t.domain, t.task_type)
    score = _difficulty_score(t)
    tier = base.tier

    reasons.append(f"domain/task baseline: {t.domain.value}/{t.task_type.value} -> {tier.value}/{base.effort.value}")
    reasons.append(f"difficulty score={score}")

    # Universal escalation rules.
    if score >= 28 and _tier_index(tier) < _tier_index(ModelTier.SOL):
        tier = ModelTier.SOL
        reasons.append("high aggregate difficulty requires at least Sol")
    if t.failure_count >= 2 and _tier_index(tier) < _tier_index(ModelTier.SOL):
        tier = ModelTier.SOL
        reasons.append("two verified failures escalated primary to Sol")
    if t.failure_count >= 4:
        tier = ModelTier.ASTRA
        reasons.append("repeated verified failure triggered Astra rescue")

    # Architecture and novel mechanical design should not be cheaped out.
    if t.task_type.value in {"architecture", "mechanism_design", "optimization"}:
        if (t.novelty >= 4 or t.uncertainty >= 4 or t.complexity >= 5) and score >= 24:
            tier = max((tier, ModelTier.SOL), key=_tier_index)
            reasons.append("novel/high-uncertainty design requires senior reasoning")

    tier = _apply_budget(tier, score, t, reasons)
    effort = _choose_effort(base.effort, score, t)

    # Astra should usually be a bounded specialist, not an expensive bulk writer.
    specialist = None
    handoff = None
    needs_astra_specialist = (
        tier == ModelTier.ASTRA
        or (
            score >= 27
            and (
                t.uncertainty >= 4
                or t.novelty >= 4
                or t.failure_count >= 2
                or t.task_type.value in {"architecture", "mechanism_design", "debug", "optimization"}
            )
        )
    )

    if needs_astra_specialist and t.task_type.value not in {"extraction", "testing"}:
        specialist_effort = ReasoningEffort.HIGH if score >= 35 or t.budget_mode == BudgetMode.MAX else ReasoningEffort.MEDIUM
        specialist = _assignment(ModelTier.ASTRA, specialist_effort, "bounded-specialist", write_allowed=False)
        reasons.append("Astra reserved as bounded read-only specialist for the hard reasoning step")

        # Unless the task itself requires a one-shot rescue implementation, return writing to Sol.
        if tier == ModelTier.ASTRA and t.failure_count < 4 and t.safety_criticality < 4:
            tier = ModelTier.SOL
            effort = ReasoningEffort.HIGH
            handoff = _assignment(ModelTier.SOL, ReasoningEffort.HIGH, "implementation-owner", write_allowed=True)
            reasons.append("implementation handed back to Sol after Astra analysis to control cost")

    primary_role = "integration-owner" if t.task_type.value in {"integration", "architecture", "review"} else "primary-worker"
    primary = _assignment(tier, effort, primary_role, write_allowed=True)

    parallelism = _parallelism(t)
    verification = _verification(t, score, tier)

    # Escalation chain is a plan after *verified* failure, not after mere uncertainty.
    chain: list[str] = []
    if tier == ModelTier.LUNA:
        chain = ["terra:high", "sol:high", "astra:medium-specialist"]
    elif tier == ModelTier.TERRA:
        chain = ["sol:high", "astra:medium-specialist"]
    elif tier == ModelTier.SOL:
        chain = ["sol:high-retry-with-new-evidence", "astra:medium-specialist", "astra:high-rescue"]
    else:
        chain = ["astra:high-rescue", "astra:xhigh-last-resort"]

    return RouteDecision(
        factory=t.domain,
        primary=primary,
        specialist=specialist,
        implementation_handoff=handoff,
        parallelism=parallelism,
        verification=verification,
        escalation_chain=tuple(chain),
        score=score,
        reasons=tuple(reasons),
    )

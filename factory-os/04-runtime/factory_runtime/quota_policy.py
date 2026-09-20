from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .models import QuotaSnapshot


class QuotaPosture(str, Enum):
    UNKNOWN = "unknown"
    GREEN = "green"
    AMBER = "amber"
    RED = "red"
    EXHAUSTED = "exhausted"


@dataclass(frozen=True)
class QuotaAssessment:
    posture: QuotaPosture
    max_used_percent: float | None
    reasons: tuple[str, ...]


def classify_quota_posture(quota: QuotaSnapshot | None) -> QuotaAssessment:
    if quota is None:
        return QuotaAssessment(QuotaPosture.UNKNOWN, None, ("quota snapshot unavailable",))
    reasons: list[str] = []
    if quota.ordinary_usage_allowed is False:
        return QuotaAssessment(QuotaPosture.EXHAUSTED, 100.0, ("ordinaryUsageAllowed=false",))
    if quota.rate_limit_reached_type:
        return QuotaAssessment(QuotaPosture.EXHAUSTED, 100.0, (f"rateLimitReachedType={quota.rate_limit_reached_type}",))

    percentages: list[float] = []
    if quota.general:
        for window in (quota.general.primary, quota.general.secondary):
            if window and window.used_percent is not None:
                percentages.append(float(window.used_percent))
    if not percentages:
        return QuotaAssessment(QuotaPosture.UNKNOWN, None, ("no supported usage window was returned",))

    used = max(percentages)
    reasons.append(f"maximum reported general quota usage is {used:.1f}%")
    if used >= 99:
        posture = QuotaPosture.EXHAUSTED
    elif used >= 90:
        posture = QuotaPosture.RED
    elif used >= 70:
        posture = QuotaPosture.AMBER
    else:
        posture = QuotaPosture.GREEN
    return QuotaAssessment(posture, used, tuple(reasons))


def astra_allowed(
    quota: QuotaSnapshot | None,
    *,
    score: int,
    failure_count: int,
    budget_mode: str,
    explicit_max_quality: bool = False,
) -> tuple[bool, str]:
    assessment = classify_quota_posture(quota)
    if explicit_max_quality or budget_mode == "max":
        if assessment.posture == QuotaPosture.EXHAUSTED:
            return False, "ordinary Codex usage appears exhausted"
        return True, "maximum-quality mode permits Astra while usage is available"
    if assessment.posture == QuotaPosture.EXHAUSTED:
        return False, "ordinary Codex usage appears exhausted"
    if assessment.posture == QuotaPosture.RED:
        return False, "quota posture is red; suppress optional Astra escalation"
    if assessment.posture == QuotaPosture.AMBER:
        if score >= 32 or failure_count >= 2:
            return True, "quota is amber but task severity justifies bounded Astra use"
        return False, "quota is amber and task does not justify Astra consumption"
    if assessment.posture == QuotaPosture.UNKNOWN:
        return score >= 30 or failure_count >= 2, "quota unknown; allow Astra only for clearly hard work"
    return True, "quota posture is green"

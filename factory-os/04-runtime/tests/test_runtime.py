from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT / "01-router"))

from factory_runtime.appserver import AppServerProbe, ProbeError
from factory_runtime.classifier import classify_prompt
from factory_runtime.models import QuotaSnapshot, RuntimeSnapshot
from factory_runtime.quota_policy import QuotaPosture, astra_allowed, classify_quota_posture
from factory_runtime.resolver import RuntimeResolver
from factory_router.models import TaskContract
from factory_router.router import route_task


def test_fake_appserver_probe_roundtrip():
    fake = HERE / "tests" / "fake_codex.py"
    snap = AppServerProbe(str(fake), timeout=3.0).probe()
    assert snap.codex_version == "0.153.4"
    assert "gpt-6-astra" in snap.model_ids
    assert snap.model("gpt-5.6-sol").supported_reasoning_efforts == ("medium", "high")
    assert snap.quota is not None
    assert snap.quota.plan_type == "prolite"
    assert classify_quota_posture(snap.quota).posture == QuotaPosture.AMBER


def test_missing_codex_is_fail_visible():
    try:
        AppServerProbe("definitely-not-a-codex-binary-xyz", timeout=0.1).probe()
    except ProbeError as exc:
        assert "not found" in str(exc)
    else:
        raise AssertionError("missing binary must raise ProbeError")


def test_quota_postures():
    for used, expected in [(20,"green"),(70,"amber"),(90,"red"),(99,"exhausted")]:
        q = QuotaSnapshot.from_appserver({"rateLimits":{"primary":{"usedPercent":used}}})
        assert classify_quota_posture(q).posture.value == expected


def test_astra_gating_balanced():
    amber = QuotaSnapshot.from_appserver({"rateLimits":{"primary":{"usedPercent":75}}})
    assert astra_allowed(amber, score=20, failure_count=0, budget_mode="balanced")[0] is False
    assert astra_allowed(amber, score=34, failure_count=0, budget_mode="balanced")[0] is True
    red = QuotaSnapshot.from_appserver({"rateLimits":{"primary":{"usedPercent":95}}})
    assert astra_allowed(red, score=40, failure_count=3, budget_mode="balanced")[0] is False


def test_factory_hinting():
    assert classify_prompt("Fix this Python API bug and add tests").factory == "software"
    assert classify_prompt("STEPモデルのサイドボタン機構とFDMの公差を設計して").factory == "cad_3dp"
    assert classify_prompt("論文を調べて比較して").factory == "research"


def test_runtime_resolver_suppresses_optional_astra_on_red():
    task = TaskContract.from_dict({
        "domain":"software","task_type":"debug","complexity":5,"uncertainty":5,"novelty":4,
        "blast_radius":3,"failure_count":2,"verification_strength":3,"parallelizability":2,
        "write_overlap_risk":2,"context_size":3,"budget_mode":"balanced"
    })
    route = route_task(task).to_dict()
    snap = AppServerProbe(str(HERE / "tests" / "fake_codex.py"), timeout=3.0).probe(include_quota=False)
    red_quota = QuotaSnapshot.from_appserver({"rateLimits":{"primary":{"usedPercent":95}}})
    snap = RuntimeSnapshot(models=snap.models, quota=red_quota)
    resolved = RuntimeResolver(snap).resolve(route, {
        "failure_count":task.failure_count,"budget_mode":task.budget_mode.value,
        "user_requires_max_quality":task.user_requires_max_quality
    })
    assert resolved.primary.model in snap.model_ids
    assert resolved.specialist is None
    assert resolved.specialist_suppressed is True


def test_runtime_resolver_effort_fallback():
    snap = AppServerProbe(str(HERE / "tests" / "fake_codex.py"), timeout=3.0).probe(include_quota=False)
    route = {
        "score": 12,
        "primary": {"model_id":"gpt-5.6-luna","reasoning_effort":"high"},
        "specialist": None,
    }
    resolved = RuntimeResolver(snap).resolve(route, {"budget_mode":"balanced","failure_count":0})
    assert resolved.primary.model == "gpt-5.6-luna"
    assert resolved.primary.effort == "medium"
    assert resolved.primary.degraded is True


def test_hooks_json_is_valid_and_has_core_events():
    data = json.loads((HERE / "config" / "hooks.json").read_text(encoding="utf-8"))
    hooks = data["hooks"]
    for event in ("SessionStart","UserPromptSubmit","PreToolUse","SubagentStart","SubagentStop"):
        assert event in hooks
    assert hooks["PreToolUse"][0]["matcher"] == "Agent|spawn_agent"


def test_agent_catalog_contract_models_are_known():
    cat = json.loads((PROJECT / "02-agents" / "catalog" / "agent_catalog.json").read_text(encoding="utf-8"))
    agents = cat["agents"] if isinstance(cat, dict) and isinstance(cat.get("agents"), list) else list(cat.values())
    allowed = {"gpt-5.6-luna","gpt-5.6-terra","gpt-5.6","gpt-5.6-sol","gpt-6-astra"}
    assert agents
    for agent in agents:
        assert (agent.get("model") or agent.get("model_id")) in allowed

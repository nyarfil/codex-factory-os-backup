from __future__ import annotations
import os,sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from factory_runtime.hook_common import emit,read_event
from factory_runtime.appserver import AppServerProbe,ProbeError
from factory_runtime.quota_policy import classify_quota_posture,QuotaPosture

e=read_event(); ti=e.get('tool_input') if isinstance(e.get('tool_input'),dict) else {}
name=str(ti.get('agent_type') or ti.get('agentType') or ti.get('name') or ti.get('agent') or '').lower()
if 'astra' not in name:
 emit('PreToolUse',additional_context='Delegate a bounded independent task. Parallel reads are fine; serialize overlapping writes; return concise evidence/results, not transcripts.')
 raise SystemExit(0)
# Astra is scarce: check current availability/quota only at the expensive decision boundary.
try:
 snap=AppServerProbe(timeout=2.0).probe(include_quota=True)
 ids=set(snap.model_ids); posture=classify_quota_posture(snap.quota).posture
 if 'gpt-6-astra' not in ids:
  emit('PreToolUse',deny=True,reason='Astra is not currently available in model/list. Retry with the corresponding Sol specialist/owner.')
 elif posture == QuotaPosture.EXHAUSTED:
  emit('PreToolUse',deny=True,reason='Astra escalation blocked because ordinary Codex usage appears exhausted. Retry with Sol High or wait for quota reset.')
 elif posture == QuotaPosture.RED:
  emit('PreToolUse',additional_context='Quota posture is red. Keep this Astra call strictly bounded to the hard reasoning bottleneck; do not fan out additional Astra workers. If Sol High can finish reliably, prefer Sol.')
 else:
  emit('PreToolUse',additional_context=f'Astra approved as a bounded read-only specialist; quota posture={posture.value}. Return the hard diagnosis/design decision to Sol/Terra for implementation.')
except ProbeError:
 # Fail open, but explicitly constrain the expensive worker.
 emit('PreToolUse',additional_context='Astra availability/quota probe unavailable. Use Astra only as a bounded read-only specialist; if spawn fails, fall back to Sol High.')

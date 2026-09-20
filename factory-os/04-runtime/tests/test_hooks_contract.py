from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]

def run(name,event):
 env={**os.environ,'CODEX_HOME':str(HERE/'tests'/'tmp-codex-home')}
 cp=subprocess.run([sys.executable,str(HERE/'hooks'/name)],input=json.dumps(event),capture_output=True,text=True,env=env,timeout=5)
 assert cp.returncode==0,cp.stderr
 return json.loads(cp.stdout or '{}')

def test_session_start_uses_hook_specific_output():
 x=run('session_start.py',{'hook_event_name':'SessionStart'}); assert x['hookSpecificOutput']['hookEventName']=='SessionStart'; assert x['hookSpecificOutput']['additionalContext']

def test_user_prompt_submit_is_tiny_and_routed():
 x=run('user_prompt_submit.py',{'hook_event_name':'UserPromptSubmit','prompt':'fix Python bug'}); c=x['hookSpecificOutput']['additionalContext']; assert 'route=software' in c; assert len(c)<350

def test_pretool_non_astra_no_probe_needed():
 x=run('pre_tool_use_agent.py',{'hook_event_name':'PreToolUse','tool_input':{'agent_type':'software_builder'}}); assert x['hookSpecificOutput']['hookEventName']=='PreToolUse'; assert 'bounded' in x['hookSpecificOutput']['additionalContext']

def test_subagent_start_mismatch_is_visible():
 x=run('subagent_start.py',{'hook_event_name':'SubagentStart','agent_type':'cad_astra_mechanism_specialist','model':'gpt-5.6'}); assert 'MODEL MISMATCH' in x['hookSpecificOutput']['additionalContext']

def test_subagent_stop_outputs_valid_json():
 x=run('subagent_stop.py',{'hook_event_name':'SubagentStop','agent_type':'software_builder','last_assistant_message':'ok'}); assert isinstance(x,dict)

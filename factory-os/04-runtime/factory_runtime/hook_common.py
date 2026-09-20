from __future__ import annotations
import json,sys

def read_event():
 try:
  raw=sys.stdin.read(); return json.loads(raw) if raw.strip() else {}
 except Exception: return {}

def emit(event:str|None=None, *, additional_context:str|None=None, system_message:str|None=None, deny:bool=False, reason:str|None=None):
 out={}
 if system_message: out['systemMessage']=system_message
 if event and (additional_context or deny):
  spec={'hookEventName':event}
  if additional_context: spec['additionalContext']=additional_context
  if deny:
   spec['permissionDecision']='deny'; spec['permissionDecisionReason']=reason or 'Blocked by Factory OS policy.'
  out['hookSpecificOutput']=spec
 sys.stdout.write(json.dumps(out,separators=(',',':')))

from __future__ import annotations
import json,os
from pathlib import Path

def _catalog_path():
 root=os.environ.get('CODEX_FACTORY_OS_ROOT')
 if root: return Path(root)/'02-agents'/'catalog'/'agent_catalog.json'
 return Path(__file__).resolve().parents[2]/'02-agents'/'catalog'/'agent_catalog.json'
def expected_agent_model(name:str)->str|None:
 try:
  d=json.loads(_catalog_path().read_text(encoding='utf-8'))
  for a in d.get('agents',[]):
   if a.get('name')==name: return a.get('model')
 except Exception: pass
 return None

from __future__ import annotations
import json,time
from pathlib import Path

def append_event(path:Path,event:dict):
 try:
  path.parent.mkdir(parents=True,exist_ok=True); row={'ts':time.time(),**event};
  with path.open('a',encoding='utf-8') as f: f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
 except Exception: pass

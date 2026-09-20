from __future__ import annotations
import hashlib,json,os,shutil,tempfile
from pathlib import Path
def sha256_file(p:Path)->str:
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def atomic_write_text(p:Path,text:str):
 p.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(prefix=p.name+'.',dir=p.parent); os.close(fd); Path(tmp).write_text(text,encoding='utf-8'); os.replace(tmp,p)
def atomic_write_json(p:Path,obj): atomic_write_text(p,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def copy_file_atomic(src:Path,dst:Path): atomic_write_text(dst,src.read_text(encoding='utf-8')) if src.suffix in {'.md','.py','.json','.toml','.ps1'} else (dst.parent.mkdir(parents=True,exist_ok=True),shutil.copy2(src,dst))
def copy_tree(src:Path,dst:Path,ignore_names:set[str]|None=None):
 ignore_names=ignore_names or set();
 for p in src.rglob('*'):
  if any(part in ignore_names for part in p.parts): continue
  q=dst/p.relative_to(src)
  if p.is_dir(): q.mkdir(parents=True,exist_ok=True)
  elif p.is_file(): q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)

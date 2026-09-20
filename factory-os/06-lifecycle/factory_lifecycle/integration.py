from __future__ import annotations
import sys
from pathlib import Path
def govern_environment(codex_home:Path,user_home:Path,repo_root:Path|None=None,source_root:Path|None=None):
 src=source_root or Path(__file__).resolve().parents[2]; gpath=src/'05-governor'
 if str(gpath) not in sys.path: sys.path.insert(0,str(gpath))
 from factory_governor.governor import govern
 return govern(codex_home=codex_home,repo_root=repo_root,user_home=user_home,source_root=source_root)

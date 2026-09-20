from __future__ import annotations
import argparse,json,os
from pathlib import Path
from .installer import install,update
from .uninstaller import uninstall
from .doctor import doctor
from .cleanup import execute_cleanup

def main(argv=None):
 ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
 def common(p): p.add_argument('--codex-home',type=Path,default=Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))); p.add_argument('--user-home',type=Path,default=Path.home())
 p=sub.add_parser('install'); common(p); p.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[2]); p.add_argument('--force',action='store_true')
 p=sub.add_parser('update'); common(p); p.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[2]); p.add_argument('--force',action='store_true')
 p=sub.add_parser('doctor'); common(p); p.add_argument('--source-root',type=Path); p.add_argument('--repo-root',type=Path)
 p=sub.add_parser('uninstall'); common(p); p.add_argument('--keep-runtime',action='store_true')
 p=sub.add_parser('cleanup'); common(p); p.add_argument('plan',type=Path); p.add_argument('--apply',action='store_true')
 ns=ap.parse_args(argv)
 if ns.cmd=='install': r=install(ns.source_root,ns.codex_home,ns.user_home,force=ns.force)
 elif ns.cmd=='update': r=update(ns.source_root,ns.codex_home,ns.user_home,force=ns.force)
 elif ns.cmd=='doctor': r=doctor(ns.codex_home,ns.user_home,source_root=ns.source_root,repo_root=ns.repo_root)
 elif ns.cmd=='uninstall': r=uninstall(ns.codex_home,ns.user_home,keep_runtime=ns.keep_runtime)
 else: r=execute_cleanup(ns.plan,ns.codex_home,ns.user_home,apply=ns.apply)
 print(json.dumps(r.to_dict(),ensure_ascii=False,indent=2)); return 0 if r.ok else 2
if __name__=='__main__': raise SystemExit(main())

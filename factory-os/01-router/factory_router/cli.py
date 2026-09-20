from __future__ import annotations
import argparse,json,sys
from .models import TaskContract
from .router import route_task

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('--pretty',action='store_true'); ap.add_argument('file',nargs='?'); ns=ap.parse_args(argv)
    raw=open(ns.file,encoding='utf-8').read() if ns.file else sys.stdin.read(); data=json.loads(raw)
    out=route_task(TaskContract.from_dict(data)).to_dict(); print(json.dumps(out,ensure_ascii=False,indent=2 if ns.pretty else None)); return 0
if __name__=='__main__': raise SystemExit(main())

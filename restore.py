from pathlib import Path
import argparse,hashlib,json,re,shutil,sys
ROOT=Path(__file__).resolve().parent

def verify():
    entries=[]
    for line in (ROOT/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        expected,rel=line.split('  ',1)
        p=(ROOT/rel).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():raise RuntimeError('Missing or invalid path: '+rel)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise RuntimeError('Hash mismatch: '+rel)
        entries.append(rel)
    return len(entries)

def main():
    ap=argparse.ArgumentParser(description='Restore Factory OS and personal references to a fresh Codex home. Existing customization is never overwritten.')
    ap.add_argument('--home',type=Path,default=Path.home());ap.add_argument('--apply',action='store_true');ns=ap.parse_args()
    count=verify();home=ns.home.expanduser().resolve();codex=home/'.codex'
    print(json.dumps({'verified_files':count,'target_home':str(home),'apply':ns.apply},ensure_ascii=False))
    if not ns.apply:return
    conflicts=[codex/n for n in ['config.toml','AGENTS.md','AGENTS.override.md','hooks.json','factory-os','user-extensions']]+[codex/'skills/user-capabilities']+list((home/'.agents/skills').glob('factory-*'))
    existing=[str(p) for p in conflicts if p.exists()]
    if existing:raise RuntimeError('Existing customization found; use a fresh home or review a manual merge: '+', '.join(existing))
    sys.path.insert(0,str(ROOT/'factory-os/06-lifecycle'))
    from factory_lifecycle.installer import install
    result=install(ROOT/'factory-os',codex,home)
    if not result.ok:raise RuntimeError(json.dumps(result.to_dict(),ensure_ascii=False))
    original=json.loads((ROOT/'records/export-policy.json').read_text(encoding='utf-8'))['original_home']
    def copy_resources(src,dst):
        shutil.copytree(src,dst)
        for p in dst.rglob('*'):
            if p.is_file() and p.suffix in {'.md','.json','.toml','.yaml','.yml'}:
                t=p.read_text(encoding='utf-8-sig')
                t=t.replace(original.replace('\\','/'),home.as_posix()).replace(original,str(home))
                p.write_text(t,encoding='utf-8')
    copy_resources(ROOT/'personal/user-extensions',codex/'user-extensions')
    copy_resources(ROOT/'personal/skills/user-capabilities',codex/'skills/user-capabilities')
    shutil.copy2(ROOT/'personal/config.template.toml',codex/'config.toml')
    bridge=(ROOT/'personal/AGENTS.bridge.md').read_text(encoding='utf-8').replace(original.replace('\\','/'),home.as_posix()).replace(original,str(home))
    with (codex/'AGENTS.md').open('a',encoding='utf-8') as f:f.write('\n'+bridge)
    manifest=codex/'user-extensions/manifest.json';d=json.loads(manifest.read_text(encoding='utf-8'));d['managed_files']=[]
    for root in [codex/'user-extensions',codex/'skills/user-capabilities']:
        for p in root.rglob('*'):
            if p.is_file() and p!=manifest:d['managed_files'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    d['restored_from']=str(ROOT);manifest.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Restored configuration and references. Follow RESTORE.md to reinstall plugins and runtime dependencies; auth and runtime binaries are not included.')
if __name__=='__main__':main()

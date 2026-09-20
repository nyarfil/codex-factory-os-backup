"""Verify archived source/input hashes and prepare an isolated ZA13 replay.

Never imports legacy scripts or executes a CAD build. Existing destinations
are rejected. Only explicitly listed inputs are copied; no hard links.
"""
import argparse,hashlib,json,shutil,sys
from pathlib import Path

SKILL=Path(__file__).resolve().parents[1]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=['upper-no-logo','upper-lightweight','precision-assembly'],required=True)
    p.add_argument('--dest',type=Path,required=True);a=p.parse_args()
    if not a.dest.is_absolute():p.error('dest must be absolute')
    dest=a.dest.resolve()
    if dest.exists():p.error('dest must not exist')
    original=Path('V:/mouse').resolve();manifest=json.loads((SKILL/'references/replay_manifest.json').read_text())
    sources=manifest['sources'];inputs=manifest['modes'][a.mode]['inputs']
    for name,digest in sources.items():
        assert sha(SKILL/'references/za13-sources'/name)==digest,('Bundled source changed',name)
    for name,digest in inputs.items():
        source=(original/name).resolve(strict=True)
        assert source.is_relative_to(original),name
        assert sha(source)==digest,('Input changed',name)
    dest.mkdir(parents=True);(dest/'scripts').mkdir()
    root=dest.as_posix()
    for name in sources:
        source=SKILL/'references/za13-sources'/name
        content=source.read_text(encoding='utf-8-sig').replace('V:/mouse',root).replace('V:\\\\mouse',root).replace('V:\\mouse',root)
        remainder=content.replace(root,'')
        assert 'V:/mouse' not in remainder and 'V:\\mouse' not in remainder
        (dest/'scripts'/name).write_text(content,encoding='utf-8')
    for name in inputs:
        target=dest/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(original/name,target);assert sha(target)==inputs[name]
    # Only the assembly manifest stores absolute checkpoint paths. Redirect it
    # after verifying/copying its original bytes; geometry/proof hashes stay fixed.
    if a.mode=='precision-assembly':
        target=dest/'outputs/ZA13_OFFICIAL_PRECISION_REPAIR_03/validated_components.json'
        data=target.read_text().replace('V:/mouse',root).replace('V:\\\\mouse',root)
        target.write_text(data,encoding='utf-8')
    recipe=manifest['modes'][a.mode]['recipe']
    (dest/'outputs/ZA13_UPPER_SURFACE_REBUILD_01').mkdir(parents=True,exist_ok=True)
    record={'mode':a.mode,'source_root':str(original),'dest':str(dest),'verified_source_count':len(sources),'verified_inputs':inputs,'recipe':recipe,'generated':False}
    (dest/'replay_preparation.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps(record))
    print('Use the installed CAD Python, set CADGEN_CACHE_DIR to the replay folder cache, and run these files in order from the destination:')
    for name in recipe:print(str(dest/'scripts'/name))
if __name__=='__main__':main()

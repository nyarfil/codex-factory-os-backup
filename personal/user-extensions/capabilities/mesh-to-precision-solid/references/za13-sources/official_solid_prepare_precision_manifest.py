"""Promote only zero-intersection component checkpoints into the final assembly recipe."""
import json,hashlib
from pathlib import Path

ROOT=Path('V:/mouse');PREV=ROOT/'outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02';OUT=ROOT/'outputs/ZA13_OFFICIAL_PRECISION_REPAIR_03'
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

entries=[
    ('Original part 160','regularized_original_160','cells'),
    ('Original part 161','regularized_original_161','cells'),
    ('Side shell','regularized_side_second','nested'),
    ('Upper shell','exact_boundary_66853','exact'),
    ('Bottom shell','exact_boundary_29246','exact'),
    ('USB connector','regularized_usb_second','nested'),
    ('Internal bracket','exact_boundary_908','exact'),
]
manifest={'reference_step_sha256':sha(PREV/'original_all_bodies.step'),'components':{},'pipeline_sources':{},'zero_volume_cleanup':json.loads((PREV/'repair_report.json').read_text())['removed_debris']}
for label,stem,kind in entries:
    geometry=PREV/(stem+'.brep');proof=PREV/(stem+'.json');data=json.loads(proof.read_text())
    if kind=='nested':data=data['regularization']
    if kind=='exact':
        assert data['valid'] and data['self_intersections']==0,label
        assert data['free_edges']==data['multiple_edges']==0,label
        count=1
    else:
        cells=[c for c in data['cells'] if c['keep']]
        assert cells and all(c['valid'] and c['self_intersections']==0 for c in cells),label
        count=len(cells)
    assert count==1,f'Unexpected fragmented part: {label}'
    manifest['components'][label]={'brep':str(geometry),'sha256':sha(geometry),'proof':str(proof),'proof_sha256':sha(proof),'solid_count':count,'valid':True,'self_intersections':0}
for name in ('official_solid_full_diagnose.py','official_solid_patch_loops.py','official_solid_exact_boundary_trial.py','official_solid_regularize.py','official_solid_contacts_regularize.py','official_solid_union_cells.py','official_solid_usb_second_pass.py','official_solid_side_second_pass.py'):
    path=ROOT/'scripts'/name;manifest['pipeline_sources'][str(path)]=sha(path)
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'validated_components.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'validated_components':len(entries),'manifest':str(OUT/'validated_components.json')}))

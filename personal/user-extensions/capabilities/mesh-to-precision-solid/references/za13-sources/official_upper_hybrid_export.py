"""STEP outputs for the one-part reconstruction pilot; Python remains authoritative."""
from pathlib import Path
import json,hashlib
from cadgen import step,build123d as bd

OUT=Path('V:/mouse/outputs/ZA13_UPPER_SURFACE_REBUILD_01')

@step(out='../outputs/ZA13_UPPER_SURFACE_REBUILD_01/ZA13_upper_lightweight_trial.step')
def lightweight():
    from official_solid_compare_geometry import read
    from official_solid_full_diagnose import shapes
    from OCP.TopAbs import TopAbs_SOLID
    from OCP.BRepCheck import BRepCheck_Analyzer
    path=OUT/'upper_hybrid_candidate.brep'
    report=json.loads((OUT/'hybrid_build_report.json').read_text())
    assert report['valid'] and report['free_edges']==0 and report['multiple_edges']==0
    shape=read(path);solids=shapes(shape,TopAbs_SOLID);assert len(solids)==1 and BRepCheck_Analyzer(solids[0]).IsValid()
    solid=bd.Solid(solids[0]);solid.label='Upper shell lightweight trial';return solid

@step(out='../outputs/ZA13_UPPER_SURFACE_REBUILD_01/ZA13_upper_reference.step')
def reference():
    from official_solid_compare_geometry import read
    from official_solid_full_diagnose import shapes
    from OCP.TopAbs import TopAbs_SOLID
    path=Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02/exact_boundary_66853.brep')
    manifest=json.loads(Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_03/validated_components.json').read_text())
    with path.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==manifest['components']['Upper shell']['sha256']
    solid=bd.Solid(shapes(read(path),TopAbs_SOLID)[0]);solid.label='Upper shell dense reference';return solid

if __name__=='__main__':
    lightweight();reference()

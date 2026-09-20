"""Independent saved STEP QA and locality evidence for the logo removal."""
import io,json,time,hashlib
from collections import Counter
from pathlib import Path
import numpy as np
from official_solid_compare_geometry import read
from official_solid_full_diagnose import shapes,bounds
from OCP.TopAbs import TopAbs_FACE,TopAbs_SOLID,TopAbs_SHELL
from OCP.TopTools import TopTools_FormatVersion_VERSION_1
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

OUT=Path('V:/mouse/outputs/ZA13_UPPER_NO_LOGO_01')
PREV=Path('V:/mouse/outputs/ZA13_UPPER_SURFACE_REBUILD_01')
def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def face_hash(face):
    s=io.BytesIO();BRepTools.Write_s(face,s,False,False,TopTools_FormatVersion_VERSION_1)
    return hashlib.sha256(s.getvalue()).hexdigest()
def main():
    start=time.monotonic()
    previous=PREV/'upper_hybrid_candidate.brep'
    assert digest(previous)=='deed242f186c535446464ee0be479ec31b5d8926ff2154dc4f33829a15aacbf4'
    original=read(previous);candidate=read(OUT/'upper_hybrid_candidate.brep')
    old=Counter(face_hash(f) for f in shapes(original,TopAbs_FACE))
    new=Counter(face_hash(f) for f in shapes(candidate,TopAbs_FACE))
    same=sum((old&new).values())
    surface_checks=[]
    for region in [4,3]:
        a=TopoDS.Face_s(read(PREV/f'candidate_surface_{region}.brep'))
        b=TopoDS.Face_s(read(OUT/f'candidate_surface_{region}.brep'))
        sa=BRep_Tool.Surface_s(a);sb=BRep_Tool.Surface_s(b)
        assert sa.NbUPoles()==sb.NbUPoles() and sa.NbVPoles()==sb.NbVPoles()
        max_pole=max(sa.Pole(i,j).Distance(sb.Pole(i,j)) for i in range(1,sa.NbUPoles()+1) for j in range(1,sa.NbVPoles()+1))
        knots_same=all(sa.UKnot(i)==sb.UKnot(i) and sa.UMultiplicity(i)==sb.UMultiplicity(i) for i in range(1,sa.NbUKnots()+1)) and all(sa.VKnot(i)==sb.VKnot(i) and sa.VMultiplicity(i)==sb.VMultiplicity(i) for i in range(1,sa.NbVKnots()+1))
        surface_checks.append({'region':region,'pole_max_difference_mm':max_pole,'knots_and_multiplicities_identical':knots_same,'whole_face_identical':face_hash(a)==face_hash(b)})
        assert max_pole==0 and knots_same
    local={'previous_brep_sha256':digest(previous),'candidate_brep_sha256':digest(OUT/'upper_hybrid_candidate.brep'),'old_faces':sum(old.values()),'new_faces':sum(new.values()),'byte_identical_faces':same,'new_or_modified_faces':sum(new.values())-same,'surfaces':surface_checks}
    (OUT/'locality_validation.json').write_text(json.dumps(local,indent=2));print(json.dumps(local),flush=True)
    assert same==sum(new.values())-1,'Only the extended outer face may differ from the previous pilot'
    assert surface_checks[1]['whole_face_identical'],'The complete inner face must remain identical'
    path=OUT/'ZA13_upper_no_logo.step';saved=read(path)
    BRepTools.Write_s(saved,str(OUT/'reimported_no_logo.brep'))
    solids=shapes(saved,TopAbs_SOLID);assert len(solids)==1
    valid=BRepCheck_Analyzer(saved).IsValid();closed=all(BRep_Tool.IsClosed_s(s) for s in shapes(saved,TopAbs_SHELL))
    assert valid and closed
    g=GProp_GProps();BRepGProp.VolumeProperties_s(saved,g);assert g.Mass()>0
    check=BRepAlgoAPI_Check();check.SetData(saved,True,True);check.SetRunParallel(True);check.Perform()
    faults=[str(r.GetCheckStatus()) for r in check.Result()]
    report={'step_sha256':digest(path),'step_bytes':path.stat().st_size,'valid':valid,'closed':closed,'solids':len(solids),'faces':len(shapes(saved,TopAbs_FACE)),'volume_mm3':g.Mass(),'bounds_mm':bounds(saved),'all_check_statuses':faults,'self_intersection_pass':not faults,'seconds':time.monotonic()-start}
    (OUT/'saved_step_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
    assert not faults
if __name__=='__main__':main()

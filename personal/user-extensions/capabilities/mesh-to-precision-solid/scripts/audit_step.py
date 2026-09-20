"""Read-only geometry audit; write one new report, exit nonzero on any finding."""
import argparse,hashlib,json,time
from pathlib import Path
from OCP.BRep import BRep_Builder,BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp
from OCP.TopTools import TopTools_IndexedMapOfShape
from OCP.TopAbs import TopAbs_SOLID,TopAbs_FACE,TopAbs_SHELL
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box

def shapes(shape,kind):
    m=TopTools_IndexedMapOfShape();TopExp.MapShapes_s(shape,kind,m)
    return [m.FindKey(i) for i in range(1,m.Extent()+1)]

def read(path):
    if path.suffix.lower()=='.brep':
        s=TopoDS_Shape();assert BRepTools.Read_s(s,str(path),BRep_Builder());return s
    if path.suffix.lower() not in ('.step','.stp'):raise ValueError('Expected STEP/STP/BREP')
    r=STEPControl_Reader();assert r.ReadFile(str(path))==IFSelect_RetDone
    assert r.TransferRoots()>0;return r.OneShape()

def audit(path,expected):
    start=time.monotonic();shape=read(path);solids=shapes(shape,TopAbs_SOLID)
    all_faces=shapes(shape,TopAbs_FACE);contained=TopTools_IndexedMapOfShape();rows=[]
    for i,s in enumerate(solids,1):
        TopExp.MapShapes_s(s,TopAbs_FACE,contained)
        g=GProp_GProps();BRepGProp.VolumeProperties_s(s,g)
        c=BRepAlgoAPI_Check();c.SetData(s,True,True);c.SetRunParallel(True);c.Perform()
        faults=[str(f.GetCheckStatus()) for f in c.Result()]
        rows.append({'solid':i,'valid':BRepCheck_Analyzer(s).IsValid(),'closed':all(BRep_Tool.IsClosed_s(x) for x in shapes(s,TopAbs_SHELL)),'volume_mm3':g.Mass(),'all_check_statuses':faults})
    stray=sum(not contained.Contains(f) for f in all_faces)
    valid=BRepCheck_Analyzer(shape).IsValid();box=Bnd_Box();BRepBndLib.AddOptimal_s(shape,box,False,False)
    with path.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    ok=valid and len(solids)==expected and not stray and all(r['valid'] and r['closed'] and r['volume_mm3']>0 and not r['all_check_statuses'] for r in rows)
    return {'ok':ok,'input':str(path),'sha256':digest,'valid':valid,'solids':len(solids),'expected_solids':expected,'faces':len(all_faces),'stray_faces':stray,'bounds_mm':None if box.IsVoid() else list(box.Get()),'parts':rows,'seconds':time.monotonic()-start,'scope':'Per-solid geometry only; no pairwise assembly interference or dimensional/deviation certification.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-solids',type=int,required=True);a=p.parse_args()
    if a.out.exists():p.error('Report already exists; choose a new path')
    if a.expected_solids<1:p.error('expected-solids must be positive')
    report=audit(a.input.resolve(strict=True),a.expected_solids)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report));raise SystemExit(0 if report['ok'] else 1)
if __name__=='__main__':main()

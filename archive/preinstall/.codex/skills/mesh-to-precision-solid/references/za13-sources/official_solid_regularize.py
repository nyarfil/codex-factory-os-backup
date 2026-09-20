"""Resolve crossing facets and retain cells with positive source winding number."""
import json,sys
from pathlib import Path
import numpy as np
from official_solid_full_diagnose import shapes,bounds
from official_solid_compare_geometry import read
from OCP.TopAbs import TopAbs_SOLID,TopAbs_FACE,TopAbs_VERTEX,TopAbs_IN,TopAbs_REVERSED
from OCP.TopoDS import TopoDS,TopoDS_Compound
from OCP.BRep import BRep_Tool,BRep_Builder
from OCP.BRepTools import BRepTools,BRepTools_WireExplorer
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.BOPAlgo import BOPAlgo_MakerVolume,BOPAlgo_CheckStatus
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopTools import TopTools_ListOfShape
from OCP.gp import gp_Pnt

OUT=Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02')

def face_points(face):
    ex=BRepTools_WireExplorer(BRepTools.OuterWire_s(face),face);p=[]
    while ex.More():p.append(BRep_Tool.Pnt_s(ex.CurrentVertex()).Coord());ex.Next()
    return np.array(p)

def normal(face):
    n=np.array(BRepAdaptor_Surface(face).Plane().Axis().Direction().Coord())
    return -n if face.Orientation()==TopAbs_REVERSED else n

def mass(s):
    p=GProp_GProps();BRepGProp.VolumeProperties_s(s,p);return p

def witness(s):
    classifier=BRepClass3d_SolidClassifier(s)
    center=mass(s).CentreOfMass();classifier.Perform(center,1e-9)
    if classifier.State()==TopAbs_IN:return np.array(center.Coord())
    for f in shapes(s,TopAbs_FACE):
        face=TopoDS.Face_s(f);prop=GProp_GProps();BRepGProp.SurfaceProperties_s(face,prop)
        c=np.array(prop.CentreOfMass().Coord());n=normal(face)
        for epsilon in (1e-5,1e-6,1e-4,1e-3):
            p=c-epsilon*n;classifier.Perform(gp_Pnt(*p),1e-9)
            if classifier.State()==TopAbs_IN:return p
    raise ValueError('No certified interior witness')

def oriented_triangles(s):
    from official_solid_patch_loops import triangles
    out=[]
    for f in shapes(s,TopAbs_FACE):
        face=TopoDS.Face_s(f);p=face_points(face);n=normal(face)
        for t in triangles(p):
            tri=p[list(t)]
            if np.dot(np.cross(tri[1]-tri[0],tri[2]-tri[0]),n)<0:tri=tri[[0,2,1]]
            out.append(tri)
    return np.array(out)

def winding(tri,p):
    v=tri-p;l=np.linalg.norm(v,axis=2);a,b,c=v[:,0],v[:,1],v[:,2]
    numerator=np.einsum('ij,ij->i',a,np.cross(b,c))
    denominator=l.prod(axis=1)+np.einsum('ij,ij->i',a,b)*l[:,2]+np.einsum('ij,ij->i',b,c)*l[:,0]+np.einsum('ij,ij->i',c,a)*l[:,1]
    return float(np.sum(2*np.arctan2(numerator,denominator))/(4*np.pi))

def regularize(source):
    tri=oriented_triangles(source)
    signed_volume=float(np.sum(np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])))/6)
    reference_volume=mass(source).Mass()
    area=GProp_GProps();BRepGProp.SurfaceProperties_s(source,area)
    maximum_tolerance=max(BRep_Tool.Tolerance_s(TopoDS.Vertex_s(v)) for v in shapes(source,TopAbs_VERTEX))
    # This gate checks orientation, not exact volume identity: planar BRep
    # integration and vertex triangles can differ within kernel edge tolerance.
    orientation_volume_bound=max(1e-7,3*area.Mass()*maximum_tolerance)
    assert abs(signed_volume-reference_volume)<orientation_volume_bound,(signed_volume,reference_volume,orientation_volume_bound)
    args=TopTools_ListOfShape()
    for f in shapes(source,TopAbs_FACE):args.Append(f)
    maker=BOPAlgo_MakerVolume();maker.SetArguments(args);maker.SetIntersect(True);maker.SetAvoidInternalShapes(True);maker.SetNonDestructive(True);maker.SetRunParallel(True)
    print(json.dumps({'stage':'resolve face crossings','source_faces':len(tri)}),flush=True)
    maker.Perform();assert not maker.HasErrors()
    cells=shapes(maker.Shape(),TopAbs_SOLID);record={'source_volume':reference_volume,'triangle_signed_volume':signed_volume,'orientation_comparison_volume_bound':orientation_volume_bound,'source_maximum_vertex_tolerance_mm':maximum_tolerance,'source_bounds':bounds(source),'cells':[]};kept=[]
    for cell in cells:
        volume=mass(cell).Mass();valid=BRepCheck_Analyzer(cell).IsValid()
        assert valid and volume>0
        point=witness(cell);w=winding(tri,point)
        assert abs(w-round(w))<1e-4,('Ambiguous source winding',w)
        keep=w>.5
        row={'volume':volume,'witness_mm':point.tolist(),'source_winding':w,'keep':keep,'faces':len(shapes(cell,TopAbs_FACE)),'valid':valid}
        if keep:
            check=BRepAlgoAPI_Check();check.SetData(cell,True,True);check.SetRunParallel(True);check.Perform()
            faults=[r for r in check.Result() if r.GetCheckStatus()==BOPAlgo_CheckStatus.BOPAlgo_SelfIntersect]
            row['self_intersections']=len(faults)
            if faults:
                row['intersection_details']=[[{'type':str(s.ShapeType()),'bounds':bounds(s),'vertices':[BRep_Tool.Pnt_s(TopoDS.Vertex_s(v)).Coord() for v in shapes(s,TopAbs_VERTEX)]} for s in [*r.GetFaultyShapes1(),*r.GetFaultyShapes2()]] for r in faults[:20]]
            kept.append(cell)
        record['cells'].append(row);print(json.dumps(row),flush=True)
    assert kept
    result=TopoDS_Compound();builder=BRep_Builder();builder.MakeCompound(result)
    for cell in kept:builder.Add(result,cell)
    record.update({'kept_solids':len(kept),'result_bounds':bounds(result),'result_volume':sum(mass(s).Mass() for s in kept)})
    return result,record

if __name__=='__main__':
    key=sys.argv[1];source=read(OUT/f'exact_boundary_{key}.brep')
    result,record=regularize(source)
    BRepTools.Write_s(result,str(OUT/f'regularized_{key}.brep'))
    (OUT/f'regularized_{key}.json').write_text(json.dumps(record,indent=2))
    print(json.dumps(record),flush=True)

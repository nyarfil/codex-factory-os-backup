"""Independent saved-STEP geometry and bidirectional surface-distance checks."""
import json,time,hashlib
from pathlib import Path
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from official_upper_surface_fit_probe import OUT
from official_solid_compare_geometry import read
from official_solid_full_diagnose import shapes,bounds
from OCP.TopAbs import TopAbs_FACE,TopAbs_SOLID,TopAbs_SHELL
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepTools import BRepTools

def mesh(shape):
    mesher=BRepMesh_IncrementalMesh(shape,.001,False,.08,False);assert mesher.IsDone()
    v=[];tri=[]
    for fs in shapes(shape,TopAbs_FACE):
        f=TopoDS.Face_s(fs);loc=TopLoc_Location();t=BRep_Tool.Triangulation_s(f,loc);assert t is not None;offset=len(v)
        v.extend(t.Node(i).Transformed(loc.Transformation()).Coord() for i in range(1,t.NbNodes()+1))
        tri.extend([[j-1+offset for j in t.Triangle(i).Get()] for i in range(1,t.NbTriangles()+1)])
    return trimesh.Trimesh(vertices=v,faces=tri,process=False)

def distances(query,target):
    # Vertices, face interiors, and all edge midpoints; deterministic samples.
    q=np.vstack([np.unique(query.vertices,axis=0),query.triangles_center,np.mean(query.vertices[query.edges_unique],axis=1)])
    vt=cKDTree(target.vertices);ft=target.triangles_tree;tri=target.triangles;out=[]
    for start in range(0,len(q),2048):
        p=q[start:start+2048];r=vt.query(p)[0]+1e-8
        candidates=[list(ft.intersection([*a,*b])) for a,b in zip(p-r[:,None],p+r[:,None])]
        counts=np.array([len(c) for c in candidates]);assert np.all(counts>0)
        indices=np.concatenate(candidates);repeat=np.repeat(p,counts,axis=0)
        near=trimesh.triangles.closest_point(tri[indices],repeat)
        out.extend(np.minimum.reduceat(np.linalg.norm(near-repeat,axis=1),np.r_[0,np.cumsum(counts)[:-1]]))
        if start%102400==0:print(f'distance samples {start}/{len(q)}',flush=True)
    a=np.array(out);assert np.isfinite(a).all()
    return {'samples':len(q),'max_mm':float(a.max()),'p99_mm':float(np.percentile(a,99)),'p99_9_mm':float(np.percentile(a,99.9)),'rms_mm':float(np.sqrt(np.mean(a*a))),'max_point_mm':q[np.argmax(a)].tolist(),'above_0_03_mm':int((a>.03).sum())}

def main():
    start=time.monotonic();path=OUT/'ZA13_upper_lightweight_trial.step';shape=read(path)
    print('Saved STEP reimported',flush=True)
    BRepTools.Write_s(shape,str(OUT/'reimported_lightweight.brep'))
    solids=shapes(shape,TopAbs_SOLID);assert len(solids)==1
    valid=BRepCheck_Analyzer(shape).IsValid();closed=all(BRep_Tool.IsClosed_s(s) for s in shapes(shape,TopAbs_SHELL));assert valid and closed
    data=np.load(OUT/'upper_reference_mesh.npz');ref=trimesh.Trimesh(vertices=data['vertices'],faces=data['faces'],process=False)
    candidate=mesh(shape);np.savez(OUT/'candidate_surface_mesh.npz',vertices=candidate.vertices,faces=candidate.faces)
    print(json.dumps({'candidate_triangles':len(candidate.faces)}),flush=True)
    report={'step_sha256':hashlib.file_digest(open(path,'rb'),'sha256').hexdigest(),'valid':valid,'closed':closed,'solids':len(solids),'faces':len(shapes(shape,TopAbs_FACE)),'bounds_mm':bounds(shape),'reference_to_candidate':distances(ref,candidate),'candidate_to_reference':distances(candidate,ref),'tessellation_deflection_mm':.001,'limitation':'Deterministic samples on a tessellated curved surface; not a continuous maximum-distance proof.','seconds':time.monotonic()-start}
    report['surface_sample_check_pass']=max(report['reference_to_candidate']['max_mm'],report['candidate_to_reference']['max_mm'])+.001<=.03
    (OUT/'saved_step_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

if __name__=='__main__':main()

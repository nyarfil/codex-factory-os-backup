"""Bidirectional sampled distance to faceted CAD surfaces, including face interiors."""
import json,sys,time,hashlib
from pathlib import Path
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from official_solid_compare_geometry import read,without_zero_volume_debris
from official_solid_full_diagnose import shapes
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh

def mesh(shape):
    mesher=BRepMesh_IncrementalMesh(shape,0.0001,False,0.1,False)
    assert mesher.IsDone()
    vertices=[];triangles=[];offset=0
    for f in shapes(shape,TopAbs_FACE):
        loc=TopLoc_Location();t=BRep_Tool.Triangulation_s(TopoDS.Face_s(f),loc)
        assert t is not None
        points=[t.Node(i).Transformed(loc.Transformation()).Coord() for i in range(1,t.NbNodes()+1)]
        vertices.extend(points);triangles.extend([[x-1+offset for x in t.Triangle(i).Get()] for i in range(1,t.NbTriangles()+1)])
        offset+=len(points)
    return trimesh.Trimesh(vertices=np.array(vertices),faces=np.array(triangles),process=False)

def stats(query,target):
    sampled=np.vstack([np.unique(query.vertices,axis=0),query.triangles_center])
    distances=[];vertex_tree=cKDTree(target.vertices);face_tree=target.triangles_tree;target_triangles=target.triangles
    for start in range(0,len(sampled),2048):
        batch=sampled[start:start+2048];radius=vertex_tree.query(batch)[0]+1e-8
        lo=batch-radius[:,None];hi=batch+radius[:,None]
        # A sphere extending to a known target vertex bounds the exact nearest
        # surface search. Reuse the trees rather than rebuilding them per chunk.
        candidates=[list(face_tree.intersection([*a,*b])) for a,b in zip(lo,hi)]
        counts=np.array([len(c) for c in candidates]);assert np.all(counts>0)
        ids=np.concatenate(candidates);points=np.repeat(batch,counts,axis=0)
        closest=trimesh.triangles.closest_point(target_triangles[ids],points)
        pair_dist=np.linalg.norm(closest-points,axis=1);assert np.isfinite(pair_dist).all()
        d=np.minimum.reduceat(pair_dist,np.r_[0,np.cumsum(counts)[:-1]]);distances.extend(d)
        if start%102400==0:print(f'distance samples {start}/{len(sampled)}',flush=True)
    d=np.array(distances)
    # This region is explicitly reported separately: source USB geometry has
    # inverted/intersecting fragments that were intentionally regularized.
    usb=(np.abs(sampled[:,0])<5)&(sampled[:,1]>-53)&(sampled[:,1]<-32)&(sampled[:,2]>3)&(sampled[:,2]<11)
    bracket=(sampled[:,0]>10.37)&(sampled[:,0]<21.20)&(sampled[:,1]>-52.14)&(sampled[:,1]<-44.96)&(sampled[:,2]>2.36)&(sampled[:,2]<3.91)
    i=int(np.argmax(d))
    return {'sample_count':len(sampled),'max_mm':float(d[i]),'max_point_mm':sampled[i].tolist(),'percentile_99_9_mm':float(np.percentile(d,99.9)),'outside_usb_region_max_mm':float(d[~usb].max()),'usb_region_max_mm':float(d[usb].max()),'bracket_region_max_mm':float(d[bracket].max()),'outside_usb_and_bracket_max_mm':float(d[~(usb|bracket)].max()),'samples_over_0_006mm':int((d>.006).sum()),'over_threshold_samples':[{'point_mm':p.tolist(),'distance_mm':float(v),'usb_region':bool(u),'bracket_region':bool(b)} for p,v,u,b in zip(sampled[d>.006],d[d>.006],usb[d>.006],bracket[d>.006])]}

if __name__=='__main__':
    before_path,after_path,out_path=map(Path,sys.argv[1:4]);started=time.monotonic()
    reference_cache=out_path.parent/'reference_surface_mesh.npz';stamp=reference_cache.with_suffix('.json')
    with before_path.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    if reference_cache.is_file() and stamp.is_file() and json.loads(stamp.read_text())['source_sha256']==digest:
        data=np.load(reference_cache);bm=trimesh.Trimesh(vertices=data['vertices'],faces=data['faces'],process=False)
    else:
        before,_=without_zero_volume_debris(read(before_path));bm=mesh(before)
        np.savez(reference_cache,vertices=bm.vertices,faces=bm.faces)
        stamp.write_text(json.dumps({'source_sha256':digest,'deflection_mm':0.0001,'excluded_zero_volume_fragments':7}))
    if '--prepare-reference' in sys.argv:
        print('Reference surface mesh cached',flush=True);sys.exit(0)
    after=read(after_path);am=mesh(after);print('Faceted CAD surfaces tessellated',flush=True)
    report={'reference_to_result':stats(bm,am),'result_to_reference':stats(am,bm),'tessellation_deflection_mm':0.0001,'seconds':time.monotonic()-started,'limitation':'Vertices and face-centroid samples; not a continuous Hausdorff maximum. USB region is reported separately, not hidden.'}
    out_path.write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

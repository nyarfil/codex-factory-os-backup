"""Inspect immutable upper shell before fitting any replacement surface."""
import json,hashlib
from pathlib import Path
import numpy as np
import trimesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from official_solid_compare_geometry import read
from official_solid_full_diagnose import shapes
from OCP.TopAbs import TopAbs_FACE,TopAbs_REVERSED
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh

OUT=Path('V:/mouse/outputs/ZA13_UPPER_SURFACE_REBUILD_01');OUT.mkdir(exist_ok=True)
source=Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02/exact_boundary_66853.brep')
manifest=json.loads(Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_03/validated_components.json').read_text())
with source.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
assert digest==manifest['components']['Upper shell']['sha256']
shape=read(source);mesher=BRepMesh_IncrementalMesh(shape,.0001,False,.1,False);assert mesher.IsDone()
v=[];tri=[]
for fs in shapes(shape,TopAbs_FACE):
    face=TopoDS.Face_s(fs);loc=TopLoc_Location();t=BRep_Tool.Triangulation_s(face,loc);offset=len(v)
    v.extend(t.Node(i).Transformed(loc.Transformation()).Coord() for i in range(1,t.NbNodes()+1))
    for i in range(1,t.NbTriangles()+1):
        ids=list(t.Triangle(i).Get())
        if face.Orientation()==TopAbs_REVERSED:ids.reverse()
        tri.append([j-1+offset for j in ids])
m=trimesh.Trimesh(vertices=v,faces=tri,process=True);assert m.is_watertight and m.is_winding_consistent
np.savez(OUT/'upper_reference_mesh.npz',vertices=m.vertices,faces=m.faces)
adj=m.face_adjacency;normals=m.face_normals
categories=np.where(normals[:,2]>.12,1,np.where(normals[:,2]<-.12,-1,0))
good=categories[adj[:,0]]==categories[adj[:,1]]
a=adj[good];matrix=coo_matrix((np.ones(len(a)),(a[:,0],a[:,1])),shape=(len(m.faces),len(m.faces)))
n,labels=connected_components(matrix,directed=False)
rows=[]
for label in range(n):
    ids=np.where(labels==label)[0]
    if len(ids)<10:continue
    pts=m.vertices[np.unique(m.faces[ids])]
    rows.append({'id':label,'faces':len(ids),'category':int(categories[ids[0]]),'area_mm2':float(m.area_faces[ids].sum()),'bounds_mm':[pts.min(axis=0).tolist(),pts.max(axis=0).tolist()]})
rows.sort(key=lambda x:x['faces'],reverse=True)
np.save(OUT/'region_labels.npy',labels)
(OUT/'diagnosis.json').write_text(json.dumps({'source':str(source),'sha256':digest,'vertices':len(m.vertices),'faces':len(m.faces),'is_watertight':m.is_watertight,'regions':rows},indent=2))
print(json.dumps(rows[:15]),flush=True)

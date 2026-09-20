"""Separate sharp detail features before fitting broad surfaces."""
import json
from pathlib import Path
import numpy as np
import trimesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from official_upper_surface_fit_probe import fit,basis

OUT=Path('V:/mouse/outputs/ZA13_UPPER_SURFACE_REBUILD_01')
d=np.load(OUT/'upper_reference_mesh.npz');m=trimesh.Trimesh(vertices=d['vertices'],faces=d['faces'],process=False)
adj=m.face_adjacency;norm=m.face_normals;old=np.load(OUT/'region_labels.npy');rows=[]
for angle in [5,10,20]:
    good=(old[adj[:,0]]==old[adj[:,1]])&(m.face_adjacency_angles<np.radians(angle))
    a=adj[good];matrix=coo_matrix((np.ones(len(a)),(a[:,0],a[:,1])),shape=(len(m.faces),len(m.faces)))
    n,labels=connected_components(matrix,directed=False)
    counts=np.bincount(labels);largest=np.argsort(counts)[-8:][::-1]
    np.save(OUT/f'feature_labels_{angle}.npy',labels)
    for label in largest:
        ids=np.where(labels==label)[0];pts=np.vstack([m.vertices[np.unique(m.faces[ids])],m.triangles_center[ids]])
        tx,ty,c,info=fit(pts,2)
        err=np.abs(basis(pts[:,:2],tx,ty)@c-pts[:,2])
        row={'angle_degrees':angle,'region':int(label),'faces':len(ids),'max_vertical_error_mm':float(err.max()),'p99_mm':float(np.percentile(err,99)),'bounds_mm':[pts.min(axis=0).tolist(),pts.max(axis=0).tolist()]};rows.append(row);print(json.dumps(row),flush=True)
(OUT/'feature_region_probe.json').write_text(json.dumps(rows,indent=2))

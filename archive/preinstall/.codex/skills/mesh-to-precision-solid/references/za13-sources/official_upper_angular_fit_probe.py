"""Try shape-aligned parameters to avoid steep-side height fitting distortion."""
import json,time
import numpy as np
import trimesh
from official_upper_surface_fit_probe import OUT,fit,basis
d=np.load(OUT/'upper_reference_mesh.npz');m=trimesh.Trimesh(vertices=d['vertices'],faces=d['faces'],process=False)
labels=np.load(OUT/'feature_labels_5.npy');rows=[]
for region in [4,3]:
    ids=np.where(labels==region)[0];p=np.vstack([m.vertices[np.unique(m.faces[ids])],m.triangles_center[ids]])
    uv=np.degrees(np.arctan2(p[:,:2]-[0,5],p[:,2,None]+5))
    for spacing in [8,4,2]:
        start=time.monotonic();cs=[]
        for axis in range(3):
            tx,ty,c,info=fit(np.column_stack([uv,p[:,axis]]),spacing);cs.append(c)
        c=np.array(cs).T;pred=basis(uv,tx,ty)@c;err=np.linalg.norm(pred-p,axis=1)
        row={'region':region,'spacing_degrees':spacing,**info,'euclidean_error_max_mm':float(err.max()),'p99_mm':float(np.percentile(err,99)),'max_point':p[np.argmax(err)].tolist(),'seconds':time.monotonic()-start};rows.append(row)
        np.savez(OUT/f'angular_fit_region{region}_spacing{spacing}.npz',tx=tx,ty=ty,coefficients=c)
        print(json.dumps(row),flush=True)
(OUT/'angular_fit_probe.json').write_text(json.dumps(rows,indent=2))

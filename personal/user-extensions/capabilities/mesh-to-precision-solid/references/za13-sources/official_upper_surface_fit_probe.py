"""Bounded least-squares B-spline feasibility probe; never a delivery model."""
import json,sys,time
from pathlib import Path
import numpy as np
import trimesh
from scipy.interpolate import BSpline
from scipy.sparse import coo_matrix,vstack,kron,eye,diags
from scipy.sparse.linalg import spsolve

OUT=Path('V:/mouse/outputs/ZA13_UPPER_SURFACE_REBUILD_01')

def knots(a,b,spacing):
    count=max(1,int(np.ceil((b-a)/spacing)))
    return np.r_[[a]*4,np.linspace(a,b,count+1)[1:-1],[b]*4]

def basis(xy,tx,ty):
    bx=BSpline.design_matrix(xy[:,0],tx,3).tocsr();by=BSpline.design_matrix(xy[:,1],ty,3).tocsr()
    nx=len(tx)-4;ny=len(ty)-4
    ix=bx.indices.reshape(-1,4);iy=by.indices.reshape(-1,4)
    data=(bx.data.reshape(-1,4,1)*by.data.reshape(-1,1,4)).reshape(-1)
    col=(ix[:,:,None]*ny+iy[:,None,:]).reshape(-1)
    rows=np.repeat(np.arange(len(xy)),16)
    return coo_matrix((data,(rows,col)),shape=(len(xy),nx*ny)).tocsr()

def fit(points,spacing):
    tx=knots(points[:,0].min(),points[:,0].max(),spacing);ty=knots(points[:,1].min(),points[:,1].max(),spacing)
    nx=len(tx)-4;ny=len(ty)-4;A=basis(points[:,:2],tx,ty)
    dx=diags([np.ones(nx-2),-2*np.ones(nx-2),np.ones(nx-2)],[0,1,2],shape=(nx-2,nx))
    dy=diags([np.ones(ny-2),-2*np.ones(ny-2),np.ones(ny-2)],[0,1,2],shape=(ny-2,ny))
    R=vstack([kron(dx,eye(ny)),kron(eye(nx),dy)]).tocsr()
    normal=(A.T@A+1e-6*(R.T@R)+1e-12*eye(nx*ny)).tocsc()
    coefficients=spsolve(normal,A.T@points[:,2])
    assert np.isfinite(coefficients).all()
    return tx,ty,coefficients,{'solver':'sparse direct regularized least squares','control_points':nx*ny}

if __name__=='__main__':
    data=np.load(OUT/'upper_reference_mesh.npz');m=trimesh.Trimesh(vertices=data['vertices'],faces=data['faces'],process=False)
    labels=np.load(OUT/'region_labels.npy');rows=[]
    for region in [0,2]:
        ids=np.where(labels==region)[0];vertex_ids=np.unique(m.faces[ids]);points=m.vertices[vertex_ids]
        sample=np.vstack([points,m.triangles_center[ids]])
        # A height surface is impossible if the same XY maps to multiple Z.
        unique,inverse=np.unique(np.round(points[:,:2],6),axis=0,return_inverse=True)
        zlo=np.full(len(unique),np.inf);zhi=np.full(len(unique),-np.inf)
        np.minimum.at(zlo,inverse,points[:,2]);np.maximum.at(zhi,inverse,points[:,2])
        print(json.dumps({'region':region,'points':len(points),'same_xy_max_z_range_mm':float((zhi-zlo).max())}),flush=True)
        for spacing in [6,3,1.5]:
            started=time.monotonic();tx,ty,c,info=fit(sample,spacing)
            err=np.abs(basis(sample[:,:2],tx,ty)@c-sample[:,2])
            row={'region':region,'spacing_mm':spacing,**info,'vertical_error_max_mm':float(err.max()),'vertical_error_p99_mm':float(np.percentile(err,99)),'max_point_mm':sample[np.argmax(err)].tolist(),'seconds':time.monotonic()-started};rows.append(row)
            np.savez(OUT/f'fit_probe_region{region}_spacing{spacing}.npz',tx=tx,ty=ty,coefficients=c)
            (OUT/'fit_probe_report.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)

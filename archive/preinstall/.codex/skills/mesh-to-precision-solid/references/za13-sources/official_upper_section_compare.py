"""Compare three physical cross sections of original and reconstructed shell."""
import os
os.environ['MPLCONFIGDIR']='V:/mouse/outputs/.matplotlib-cache'
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from official_upper_surface_fit_probe import OUT
def load(name):
    d=np.load(OUT/name);return trimesh.Trimesh(vertices=d['vertices'],faces=d['faces'],process=False)
ref=load('upper_reference_mesh.npz');trial=load('candidate_surface_mesh.npz')
fig,axes=plt.subplots(3,1,figsize=(12,10),dpi=150)
for ax,x in zip(axes,[-20,0,10]):
    for mesh,color,label,width in [(ref,'#202a36','Reference',1.5),(trial,'#12a1a1','Rebuilt',.8)]:
        lines=trimesh.intersections.mesh_plane(mesh,[1,0,0],[x,0,0])
        ax.add_collection(LineCollection(lines[:,:,[1,2]],colors=color,linewidths=width,label=label))
    ax.autoscale();ax.set_aspect('equal');ax.set_title(f'X = {x} mm');ax.set_xlabel('Y (mm)');ax.set_ylabel('Z (mm)');ax.grid(alpha=.2);ax.legend(loc='upper left')
fig.suptitle('Upper shell: reference and rebuilt cross sections overlap',fontsize=16)
fig.tight_layout();fig.savefig(OUT/'section-comparison.png')
print('Section comparison saved',flush=True)

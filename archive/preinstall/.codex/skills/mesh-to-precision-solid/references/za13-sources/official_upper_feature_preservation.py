"""Check original sharp-detail vertices against the actual saved-STEP tessellation."""
import json
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from official_upper_surface_fit_probe import OUT
r=np.load(OUT/'upper_reference_mesh.npz');c=np.load(OUT/'candidate_surface_mesh.npz')
m=trimesh.Trimesh(vertices=r['vertices'],faces=r['faces'],process=False)
edges=m.face_adjacency_edges[m.face_adjacency_angles>=np.radians(5)]
ids=np.unique(edges);dist=cKDTree(c['vertices']).query(m.vertices[ids])[0]
report={'feature_definition':'Endpoints of original edges with dihedral angle >=5 degrees','tested_vertices':len(ids),'max_nearest_candidate_vertex_distance_mm':float(dist.max()),'vertices_over_0_00001_mm':int((dist>1e-5).sum()),'limitation':'This verifies retained detail vertices, not all future attachment clearances.'}
(OUT/'feature_preservation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

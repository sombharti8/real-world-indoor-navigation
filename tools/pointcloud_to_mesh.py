#!/usr/bin/env python3
"""PLY point cloud -> OBJ surface mesh using Open3D.

Usage: python3 pointcloud_to_mesh.py input.ply output.obj
"""
import sys
import numpy as np
import open3d as o3d

if len(sys.argv) != 3:
    print('Usage: python3 pointcloud_to_mesh.py input.ply output.obj')
    raise SystemExit(1)

pcd = o3d.io.read_point_cloud(sys.argv[1])
print(f'Loaded points: {len(pcd.points)}')
pcd = pcd.voxel_down_sample(voxel_size=0.03)
pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
pcd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.15, max_nn=30))
pcd.orient_normals_consistent_tangent_plane(30)
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
d = np.asarray(densities)
mesh.remove_vertices_by_mask(d < np.quantile(d, 0.02))
mesh.remove_degenerate_triangles()
mesh.remove_duplicated_triangles()
mesh.remove_duplicated_vertices()
mesh.remove_non_manifold_edges()
o3d.io.write_triangle_mesh(sys.argv[2], mesh, write_triangle_uvs=False)
print(f'Wrote {sys.argv[2]}: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles')

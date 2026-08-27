# Point Cloud Processing

The supplied `map_ros_cloud.ply` is a point cloud, not a polygon mesh. Use Open3D for surface reconstruction:

```bash
python3 -m pip install open3d numpy
python3 pointcloud_to_mesh.py /path/to/map_ros_cloud.ply environment.obj
```

The conversion script uses 3 cm voxel downsampling, statistical outlier removal, normal estimation, and Poisson reconstruction. The output should be visually inspected before use as Gazebo collision geometry.

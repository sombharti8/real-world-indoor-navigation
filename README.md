# Real-World Indoor Navigation & State Monitoring

**Student:** Som Bharti  
**Enrollment No.:** 25MMT0008

ROS 2 project for integrating a real-world indoor 3D scan into simulation, localizing a mobile robot, navigating with Nav2, and publishing custom robot state telemetry.

## Project pipeline

3D Point Cloud (PLY) → cleaned/reconstructed mesh → Gazebo static environment → 2D navigation map → AMCL + Nav2 → `robot_state_manager`

## Main ROS 2 interfaces

- `/robot/next_waypoint` — `geometry_msgs/msg/Point`
- `/robot/current_xyz` — `geometry_msgs/msg/Point`, published at 10 Hz
- `/odom` — robot odometry
- `/cmd_vel` — navigation controller velocity command
- Nav2 action: `nav2_msgs/action/NavigateToPose`

## Dataset

The supplied `map_ros_cloud.ply` was inspected as a binary little-endian PLY point cloud with approximately 2.34 million points and no polygon faces. Its approximate dimensions are 28.25 m × 16.54 m × 4.85 m. The point cloud therefore requires surface reconstruction before it can be used as a Gazebo collision mesh.

The original scan should be kept outside normal Git history when large; use Git LFS or the assignment-provided Google Drive link when required.

## Build

```bash
cd ~/indoor_navigation_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Run the state manager

```bash
ros2 launch robot_state_manager robot_state_manager.launch.py
```

## Send a waypoint

```bash
ros2 topic pub --once /robot/next_waypoint geometry_msgs/msg/Point "{x: 5.0, y: 3.0, z: 0.0}"
```

## Check telemetry

```bash
ros2 topic hz /robot/current_xyz
ros2 topic echo /robot/current_xyz
```

## Check velocity commands

```bash
ros2 topic echo /cmd_vel
```

## Verify TF

```bash
ros2 run tf2_tools view_frames
```

Expected transform chain:

`map → odom → base_link`

## Environment conversion

Install Open3D and NumPy:

```bash
python3 -m pip install open3d numpy
```

Then run:

```bash
python3 tools/pointcloud_to_mesh.py /path/to/map_ros_cloud.ply environment.obj
```

## Notes

For a ground robot, the waypoint `z` coordinate is retained for the telemetry interface but the Nav2 pose is projected to the ground plane and uses a zero-yaw orientation.

Before final submission, validate the reconstructed collision mesh, the 2D occupancy map, AMCL localization, Nav2 behavior, and the 10 Hz telemetry topic in your ROS 2 + Gazebo environment.

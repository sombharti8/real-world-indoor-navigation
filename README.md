# Real-World Indoor Navigation & State Monitoring

**Student:** Som Bharti  
**Enrollment No.:** 25MMT0008

## Objective

Integrate a real-world indoor 3D scan into a Gazebo/simulation environment, localize a standard mobile robot, navigate point-to-point using Nav2, and publish custom robot state telemetry.

## Architecture

```text
Real-world PLY scan
       ↓
Point-cloud processing
       ↓
OBJ collision model + 2D occupancy map
       ↓
Gazebo static environment
       ↓
Robot + LiDAR + odometry
       ↓
AMCL: map → odom → base_link
       ↓
Nav2 planner/controller
       ↓
robot_state_manager
       ├── /robot/current_xyz  (10 Hz)
       ├── /robot/next_waypoint
       └── /cmd_vel monitoring
```

## Dataset

The supplied `map_ros_cloud.ply` was inspected as a binary little-endian PLY with approximately 2,338,923 points and no polygon faces. Approximate dimensions are **28.25 m × 16.54 m × 4.85 m**.

The repository does not store the original large PLY. It stores processed simulation artifacts instead.

## Repository contents

- `src/robot_state_manager/` — ROS 2 Python node, launch file and parameters
- `models/scanned_environment/` — Gazebo static model and OBJ collision shell
- `worlds/` — Gazebo world
- `maps/` — generated 2D occupancy map and YAML metadata
- `config/nav2_params.yaml` — AMCL/Nav2 parameter starting point
- `tools/pointcloud_to_mesh.py` — PLY to OBJ reconstruction utility
- `docs/` — dataset inspection, test plan and generated-output notes

## Build

```bash
mkdir -p ~/indoor_navigation_ws/src
cd ~/indoor_navigation_ws/src
git clone https://github.com/sombharti8/real-world-indoor-navigation.git
cd ~/indoor_navigation_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Run robot_state_manager

```bash
ros2 launch robot_state_manager robot_state_manager.launch.py
```

## Send waypoint

```bash
ros2 topic pub --once /robot/next_waypoint geometry_msgs/msg/Point "{x: 5.0, y: 3.0, z: 0.0}"
```

The standard Nav2 action used internally is `nav2_msgs/action/NavigateToPose`. For a ground robot, waypoint z is retained by the telemetry interface but the Nav2 goal is projected to z=0 with yaw=0.

## Verify telemetry

```bash
ros2 topic hz /robot/current_xyz
ros2 topic echo /robot/current_xyz
```

Expected publishing frequency: approximately **10 Hz**.

## Monitor velocity

```bash
ros2 topic echo /cmd_vel
```

Default warnings:

- `|linear.x| > 0.50 m/s`
- `|angular.z| > 1.00 rad/s`

## Verify TF

```bash
ros2 run tf2_tools view_frames
```

Expected chain:

`map → odom → base_link`

## Point-cloud conversion

```bash
python3 -m pip install open3d numpy
python3 tools/pointcloud_to_mesh.py /path/to/map_ros_cloud.ply environment.obj
```

The committed OBJ is a lightweight collision representation derived from the scan projection so it remains practical for a GitHub assignment repository.

## Important validation note

The generated files are based on the supplied point cloud, but **full Gazebo + Nav2 + AMCL runtime validation must be performed on a ROS 2 machine** with the required Gazebo, Nav2, AMCL and robot packages installed. Runtime screenshots/logs should be added to `docs/` before final submission if your evaluator requires proof of execution.

## Student

**Som Bharti — 25MMT0008**

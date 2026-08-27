# Test Plan

**Student:** Som Bharti  
**Enrollment:** 25MMT0008

## 1. Environment
- Open the reconstructed mesh in a 3D viewer.
- Confirm dimensions are metre-scale.
- Load it as a static Gazebo collision object.
- Verify the robot cannot drive through walls.

## 2. TF
```bash
ros2 run tf2_tools view_frames
```
Verify `map -> odom -> base_link` is present and stable.

## 3. XYZ telemetry
```bash
ros2 topic hz /robot/current_xyz
ros2 topic echo /robot/current_xyz
```
Expected: approximately 10 Hz.

## 4. Waypoint navigation
```bash
ros2 topic pub --once /robot/next_waypoint geometry_msgs/msg/Point "{x: 3.0, y: 2.0, z: 0.0}"
```
Expected: waypoint received and a Nav2 NavigateToPose goal accepted if Nav2 is active.

## 5. Velocity monitor
```bash
ros2 topic echo /cmd_vel
```
The state manager warns when `|linear.x| > 0.50 m/s` or `|angular.z| > 1.00 rad/s` by default.

## 6. Localization
Drive through multiple waypoints and compare the AMCL pose with the 2D map in RViz.

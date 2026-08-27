# Generated Output

**Student:** Som Bharti  
**Enrollment:** 25MMT0008

## Point-cloud inspection

The supplied `map_ros_cloud.ply` was parsed successfully as a binary little-endian PLY containing approximately 2,338,923 points and no polygon faces.

Approximate scan bounds:

- X: -7.0849 to 21.1681 m
- Y: -5.4358 to 11.1088 m
- Z: -1.3638 to 3.4865 m

## Mesh output

`models/scanned_environment/meshes/environment.obj` is a lightweight collision shell derived from the projected scan. It preserves metre-scale XY coordinates and uses a 2.5 m collision height for indoor navigation.

The mesh is intentionally simplified so it can be stored and reviewed directly in GitHub. The original PLY should remain the source dataset and can be used for a higher-resolution reconstruction when running the full simulation locally.

## 2D map output

`maps/indoor_map.pgm` is a generated 2D projection of wall-like scan points using surface normals to suppress floor/ceiling points. The committed demonstration map uses 0.60 m/pixel to keep the GitHub artifact compact.

`maps/indoor_map.yaml` defines the map origin and resolution.

## State-manager expected output

```text
[INFO] [robot_state_manager]: robot_state_manager started; XYZ telemetry = 10 Hz
[INFO] [robot_state_manager]: Received waypoint: x=5.000, y=3.000, z=0.000
[INFO] [robot_state_manager]: Nav2 goal accepted
[WARN] [robot_state_manager]: High angular velocity: 1.142 rad/s
```

Exact navigation completion status depends on the ROS 2/Nav2 distribution and simulation run.

## Validation status

The point-cloud processing and file generation were completed from the supplied PLY. Full Gazebo + Nav2 execution still needs to be run on a ROS 2 machine with Gazebo, Nav2, AMCL and a standard robot package installed. The repository therefore distinguishes generated artifacts from runtime screenshots/logs.

# 2D Navigation Map

Nav2 requires a 2D occupancy representation. Generate `indoor_map.pgm` and `indoor_map.yaml` by projecting the 3D scan/mesh onto the robot navigation plane.

Recommended resolution: 0.05–0.10 m/pixel.

Before final submission, inspect the map in RViz and remove ceiling/overhead geometry that should not be treated as ground-level obstacles.

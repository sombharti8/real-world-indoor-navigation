from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_state_manager',
            executable='robot_state_manager',
            name='robot_state_manager',
            output='screen',
            parameters=[{
                'publish_rate_hz': 10.0,
                'linear_velocity_threshold': 0.50,
                'angular_velocity_threshold': 1.00,
                'goal_frame': 'map',
            }],
        )
    ])

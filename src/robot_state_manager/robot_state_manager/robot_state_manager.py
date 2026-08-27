#!/usr/bin/env python3
"""ROS 2 robot_state_manager: XYZ telemetry, waypoint goals and /cmd_vel monitoring."""
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import Point, Twist
from nav_msgs.msg import Odometry
from nav2_msgs.action import NavigateToPose
from tf_transformations import quaternion_from_euler

class RobotStateManager(Node):
    def __init__(self):
        super().__init__('robot_state_manager')
        self.declare_parameter('publish_rate_hz', 10.0)
        self.declare_parameter('linear_velocity_threshold', 0.50)
        self.declare_parameter('angular_velocity_threshold', 1.00)
        self.declare_parameter('goal_frame', 'map')
        self.linear_threshold = float(self.get_parameter('linear_velocity_threshold').value)
        self.angular_threshold = float(self.get_parameter('angular_velocity_threshold').value)
        self.goal_frame = str(self.get_parameter('goal_frame').value)
        self.current_xyz = Point()
        self.xyz_pub = self.create_publisher(Point, '/robot/current_xyz', 10)
        self.create_subscription(Odometry, '/odom', self.odom_callback, 20)
        self.create_subscription(Point, '/robot/next_waypoint', self.waypoint_callback, 10)
        self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 20)
        hz = float(self.get_parameter('publish_rate_hz').value)
        self.create_timer(1.0 / hz, self.publish_xyz)
        self.nav_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.get_logger().info('robot_state_manager started; XYZ telemetry = 10 Hz')

    def odom_callback(self, msg):
        p = msg.pose.pose.position
        self.current_xyz.x, self.current_xyz.y, self.current_xyz.z = p.x, p.y, p.z

    def publish_xyz(self):
        self.xyz_pub.publish(self.current_xyz)

    def cmd_vel_callback(self, msg):
        if abs(msg.linear.x) > self.linear_threshold:
            self.get_logger().warn(f'High linear velocity: {msg.linear.x:.3f} m/s')
        if abs(msg.angular.z) > self.angular_threshold:
            self.get_logger().warn(f'High angular velocity: {msg.angular.z:.3f} rad/s')

    def waypoint_callback(self, msg):
        self.get_logger().info(f'Received waypoint: x={msg.x:.3f}, y={msg.y:.3f}, z={msg.z:.3f}')
        if not self.nav_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error('Nav2 NavigateToPose action server unavailable')
            return
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = self.goal_frame
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x, goal.pose.pose.position.y = msg.x, msg.y
        q = quaternion_from_euler(0.0, 0.0, 0.0)
        goal.pose.pose.orientation.x, goal.pose.pose.orientation.y = q[0], q[1]
        goal.pose.pose.orientation.z, goal.pose.pose.orientation.w = q[2], q[3]
        future = self.nav_client.send_goal_async(goal)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        try:
            handle = future.result()
            if not handle.accepted:
                self.get_logger().warn('Nav2 goal rejected')
                return
            self.get_logger().info('Nav2 goal accepted')
            handle.get_result_async().add_done_callback(self.goal_result_callback)
        except Exception as e:
            self.get_logger().error(f'Goal request failed: {e}')

    def goal_result_callback(self, future):
        try:
            self.get_logger().info(f'Navigation finished with status code {future.result().status}')
        except Exception as e:
            self.get_logger().error(f'Navigation result error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = RobotStateManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

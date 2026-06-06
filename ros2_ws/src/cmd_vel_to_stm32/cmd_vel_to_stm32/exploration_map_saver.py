import math
import os
import subprocess

import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty
from tf2_ros import Buffer, TransformException, TransformListener


class ExplorationMapSaver(Node):
    def __init__(self):
        super().__init__('exploration_map_saver')

        self.declare_parameter('completion_topic', 'exploration_complete')
        self.declare_parameter('map_output_prefix', '/home/slamrobot/maps/autonomous_explored_map')
        self.declare_parameter('global_frame', 'map')
        self.declare_parameter('robot_base_frame', 'base_footprint')
        self.declare_parameter('save_pose', True)

        self.completion_topic = self.get_parameter('completion_topic').value
        self.map_output_prefix = self.get_parameter('map_output_prefix').value
        self.global_frame = self.get_parameter('global_frame').value
        self.robot_base_frame = self.get_parameter('robot_base_frame').value
        self.save_pose = self.get_parameter('save_pose').value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.saved = False

        self.subscription = self.create_subscription(
            Empty,
            self.completion_topic,
            self._completion_callback,
            10,
        )

        self.get_logger().info(
            f'Waiting for exploration completion on /{self.completion_topic.lstrip("/")}'
        )

    def _completion_callback(self, _msg):
        if self.saved:
            return

        self.saved = True
        os.makedirs(os.path.dirname(self.map_output_prefix), exist_ok=True)

        self.get_logger().info(f'Exploration complete; saving map to {self.map_output_prefix}')
        result = subprocess.run(
            ['ros2', 'run', 'nav2_map_server', 'map_saver_cli', '-f', self.map_output_prefix],
            check=False,
            text=True,
            capture_output=True,
        )

        if result.returncode != 0:
            self.get_logger().error(
                'map_saver_cli failed: '
                f'{result.stderr.strip() or result.stdout.strip() or "no output"}'
            )
            return

        self.get_logger().info('Map saved')
        if self.save_pose:
            self._save_pose()

    def _save_pose(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.global_frame,
                self.robot_base_frame,
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=1.0),
            )
        except TransformException as exc:
            self.get_logger().warn(f'Could not save final pose: {exc}')
            return

        t = transform.transform.translation
        q = transform.transform.rotation
        yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z),
        )

        pose_path = f'{self.map_output_prefix}_pose.txt'
        with open(pose_path, 'w', encoding='utf-8') as pose_file:
            pose_file.write(f'{t.x:.6f} {t.y:.6f} {t.z:.6f} {yaw:.6f}\n')

        self.get_logger().info(f'Final pose saved to {pose_path}')


def main(args=None):
    rclpy.init(args=args)
    node = ExplorationMapSaver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

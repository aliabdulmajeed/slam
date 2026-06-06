#!/usr/bin/env python3

import subprocess
import time

SESSION = "slam_robot"

COMMON = (
    "source /opt/ros/jazzy/setup.bash && "
    "source /home/slamrobot/ros2_ws/install/setup.bash && "
    "export ROS_DOMAIN_ID=0 && "
    "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp"
)

LIDAR_COMMON = (
    "source /opt/ros/jazzy/setup.bash && "
    "source /home/slamrobot/ws_lidar/install/setup.bash && "
    "export ROS_DOMAIN_ID=0 && "
    "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp"
)

def run(cmd):
    subprocess.run(cmd, shell=True)

def create_window(name, command):
    subprocess.run(["tmux", "new-window", "-t", SESSION, "-n", name])
    time.sleep(0.3)
    subprocess.run(["tmux", "send-keys", "-t", f"{SESSION}:{name}", command, "C-m"])

def main():
    run(f"tmux kill-session -t {SESSION} 2>/dev/null")

    run("pkill -f robot_state_publisher 2>/dev/null")
    run("pkill -f joint_state_publisher 2>/dev/null")
    run("pkill -f sllidar 2>/dev/null")
    run("pkill -f laser_scan_matcher 2>/dev/null")
    run("pkill -f slam_toolbox 2>/dev/null")
    run("pkill -f cmd_vel_bridge 2>/dev/null")
    run("pkill -f nav2 2>/dev/null")
    run("pkill -f rviz2 2>/dev/null")
    run("pkill -f frontier_explorer 2>/dev/null")

    time.sleep(1)

    subprocess.run(["tmux", "new-session", "-d", "-s", SESSION, "-n", "main"])

    create_window(
        "robot_state",
        COMMON + " && ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:=\"$(cat /home/slamrobot/ros2_ws/src/my_robot_description/urdf/robot.urdf)\""
    )

    create_window(
        "joint_state",
        COMMON + " && ros2 run joint_state_publisher joint_state_publisher"
    )

    create_window(
        "lidar",
        LIDAR_COMMON + " && ros2 launch sllidar_ros2 sllidar_a1_launch.py serial_port:=/dev/ttyUSB0 serial_baudrate:=115200 frame_id:=laser"
    )

    create_window(
        "odom",
        COMMON + " && ros2 run ros2_laser_scan_matcher laser_scan_matcher --ros-args -p base_frame:=base_footprint -p odom_frame:=odom -p publish_tf:=true -p publish_odom:=/odom"
    )

    create_window(
        "slam",
        COMMON + " && ros2 launch slam_toolbox online_async_launch.py use_sim_time:=false slam_params_file:=/home/slamrobot/slam_virtual_odom.yaml"
    )

    create_window(
        "bridge",
        COMMON + " && ros2 run cmd_vel_to_stm32 cmd_vel_bridge"
    )

    create_window(
        "nav2",
        COMMON + " && ros2 launch nav2_bringup navigation_launch.py use_sim_time:=false params_file:=/home/slamrobot/nav2_params/nav2_params.yaml"
    )

    create_window(
        "rviz",
        COMMON + " && rviz2"
    )

    create_window(
        "explorer",
        COMMON + " && ros2 run frontier_exploration_ros2 frontier_explorer --ros-args --params-file /home/slamrobot/explore_params/frontier_params.yaml -p use_sim_time:=false"
    )

    create_window(
        "map_saver",
        COMMON + " && ros2 run cmd_vel_to_stm32 exploration_map_saver --ros-args -p completion_topic:=exploration_complete -p map_output_prefix:=/home/slamrobot/maps/autonomous_explored_map -p use_sim_time:=false"
    )

    subprocess.run(["tmux", "kill-window", "-t", f"{SESSION}:main"])

    print("SLAM robot system started.")
    print(f"Attach using: tmux attach -t {SESSION}")
    print(f"List windows: tmux list-windows -t {SESSION}")
    print(f"Stop everything: tmux kill-session -t {SESSION}")

if __name__ == "__main__":
    main()

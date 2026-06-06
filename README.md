# SLAM Robot Project

This repository contains the ROS 2 source code, configuration files, RViz setup, navigation parameters, lidar driver workspace, Gazebo world assets, and supporting notes used for the SLAM robot project.

The goal of this project is to support robot visualization, lidar-based localization/scan matching, SLAM map visualization, frontier exploration, navigation costmaps, goal setting, and robot model inspection in RViz.

## Repository Structure

```text
.
├── SLAM.rviz
├── README.md
├── anydesk
├── ros2_ws/
│   └── src/
│       ├── cmd_vel_to_stm32/
│       ├── csm/
│       ├── frontier_exploration_ros2/
│       ├── my_robot_description/
│       ├── ros2_laser_scan_matcher/
│       ├── slamrobot_gazebo/
│       └── main_packet_parser.c
├── ws_lidar/
│   └── src/
│       └── sllidar_ros2/
├── nav2_params/
├── explore_params/
└── codex_changes/
```

## Main Components

| Path | Purpose |
| --- | --- |
| `SLAM.rviz` | RViz configuration for SLAM, navigation, TF, robot model, costmaps, exploration markers, selected frontiers, and planned paths. |
| `ros2_ws/src/my_robot_description` | Robot description package containing the robot URDF used by RViz. |
| `ros2_ws/src/cmd_vel_to_stm32` | ROS 2 Python package for bridging velocity commands and related robot control utilities. |
| `ros2_ws/src/frontier_exploration_ros2` | Frontier exploration package with exploration logic, launch files, configuration, services, and tests. |
| `ros2_ws/src/ros2_laser_scan_matcher` | ROS 2 laser scan matcher package. |
| `ros2_ws/src/csm` | Canonical scan matcher dependency/package. |
| `ros2_ws/src/slamrobot_gazebo` | Gazebo-related project assets, including the simulation world. |
| `ws_lidar/src/sllidar_ros2` | SLLIDAR/RPLIDAR ROS 2 driver package and launch files. |
| `nav2_params` | Navigation 2 parameter files. |
| `explore_params` | Frontier exploration parameter files. |
| `codex_changes` | Supporting project notes, scripts, backups, and generated change documentation kept for project traceability. |
| `anydesk` | ARM64 Linux AnyDesk executable included with the original project files. |

## RViz Configuration

`SLAM.rviz` uses `map` as the fixed frame. It expects the robot and navigation stack to publish the following frames:

- `map`
- `odom`
- `base_footprint`
- `base_link`
- `laser`
- `front_left_wheel`
- `front_right_wheel`
- `rear_left_wheel`
- `rear_right_wheel`

The RViz configuration subscribes to these main topics:

| Topic | Purpose |
| --- | --- |
| `/map` | SLAM occupancy grid map. |
| `/map_updates` | Incremental map updates. |
| `/global_costmap/costmap` | Global navigation costmap. |
| `/global_costmap/costmap_updates` | Global costmap updates. |
| `/local_costmap/costmap` | Local navigation costmap. |
| `/local_costmap/costmap_updates` | Local costmap updates. |
| `/explore/frontiers` | Frontier exploration marker array. |
| `/explore/selected_frontier` | Selected frontier pose. |
| `/plan` | Planned navigation path. |
| `/initialpose` | Initial pose estimate from RViz. |
| `/goal_pose` | Navigation goal pose from RViz. |
| `/clicked_point` | Published point from RViz. |

The robot model display currently references:

```text
/home/slamrobot/ros2_ws/src/my_robot_description/urdf/robot.urdf
```

If you use the project on another machine, either keep the same workspace path or update the RobotModel display path inside `SLAM.rviz`.

## Setup

Install ROS 2 and the dependencies required by the included packages. Then build the source workspace.

```bash
cd ~/Desktop/ros2_ws
colcon build
source install/setup.bash
```

If you also need the lidar workspace:

```bash
cd ~/Desktop/ws_lidar
colcon build
source install/setup.bash
```

For a normal robot session, source ROS 2 and the built workspaces:

```bash
source /opt/ros/<ros-distro>/setup.bash
source ~/Desktop/ros2_ws/install/setup.bash
source ~/Desktop/ws_lidar/install/setup.bash
```

Replace `<ros-distro>` with your installed ROS 2 distribution, for example `humble`, `iron`, or `jazzy`.

## Running RViz

From the repository root:

```bash
rviz2 -d SLAM.rviz
```

Start the robot drivers, lidar node, SLAM/localization, Nav2, and frontier exploration nodes before opening RViz if you want all displays to populate.

## Navigation and Exploration Parameters

Navigation parameters are stored in:

```text
nav2_params/
```

Frontier exploration parameters are stored in:

```text
explore_params/
```

Package-level exploration configuration is also available inside:

```text
ros2_ws/src/frontier_exploration_ros2/config/
```

## Notes

- Generated folders such as `build/`, `install/`, and `log/` are intentionally ignored by git. They should be recreated with `colcon build`.
- Nested `.git` metadata from third-party packages was excluded so all files are stored normally in this repository.
- The included `anydesk` binary is an ARM64 Linux executable and may only run on compatible systems.
- Some packages may require additional system dependencies depending on your ROS 2 distribution and robot hardware.

## License

This repository contains multiple packages and dependencies with their own license files. Review each package license before redistribution or commercial use.

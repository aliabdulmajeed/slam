# SLAM RViz Configuration

This repository contains the RViz configuration used to visualize and monitor a ROS 2 SLAM and navigation setup.

The project is centered around `SLAM.rviz`, which configures RViz for map visualization, robot model display, TF inspection, navigation costmaps, frontier exploration markers, selected frontier poses, and planned paths.

## Repository Contents

| File | Description |
| --- | --- |
| `SLAM.rviz` | RViz configuration for SLAM, navigation, robot model visualization, costmaps, frontiers, and path planning. |
| `anydesk` | ARM64 Linux AnyDesk executable included with the project files. |

## RViz Configuration Overview

`SLAM.rviz` is configured for a ROS 2 robot system with the fixed frame set to:

```text
map
```

The configuration includes the following RViz displays:

- Grid display for spatial reference.
- Robot model display loaded from a URDF file.
- TF tree visualization.
- Occupancy grid map visualization.
- Global and local navigation costmap visualization.
- Frontier exploration marker visualization.
- Selected frontier pose visualization.
- Planned path visualization.

## Expected ROS 2 Frames

The TF tree configured in RViz expects these frames:

- `map`
- `odom`
- `base_footprint`
- `base_link`
- `laser`
- `front_left_wheel`
- `front_right_wheel`
- `rear_left_wheel`
- `rear_right_wheel`

## Expected ROS 2 Topics

The RViz configuration listens to the following topics:

| Topic | Purpose |
| --- | --- |
| `/map` | Main SLAM occupancy grid map. |
| `/map_updates` | Incremental map updates. |
| `/global_costmap/costmap` | Global navigation costmap. |
| `/global_costmap/costmap_updates` | Global costmap updates. |
| `/local_costmap/costmap` | Local navigation costmap. |
| `/local_costmap/costmap_updates` | Local costmap updates. |
| `/explore/frontiers` | Frontier exploration marker array. |
| `/explore/selected_frontier` | Currently selected frontier pose. |
| `/plan` | Planned navigation path. |
| `/initialpose` | Initial pose topic used by the RViz 2D Pose Estimate tool. |
| `/goal_pose` | Goal pose topic used by the RViz 2D Goal Pose tool. |
| `/clicked_point` | Point publishing topic used by the RViz Publish Point tool. |

## Robot Model

The RViz configuration currently references the robot URDF at:

```text
/home/slamrobot/ros2_ws/src/my_robot_description/urdf/robot.urdf
```

If this repository is used on another machine, update the `RobotModel` display in `SLAM.rviz` or ensure the URDF exists at the same path.

## Usage

1. Source the ROS 2 environment:

   ```bash
   source /opt/ros/<ros-distro>/setup.bash
   ```

2. Source your workspace, if applicable:

   ```bash
   source ~/ros2_ws/install/setup.bash
   ```

3. Start the robot, SLAM, navigation, and exploration nodes that publish the expected frames and topics.

4. Launch RViz with this configuration:

   ```bash
   rviz2 -d SLAM.rviz
   ```

## Notes

- This repository stores the visualization configuration and related project files only.
- The ROS 2 packages, launch files, URDF, SLAM nodes, navigation stack, and exploration nodes must be available in the target ROS 2 workspace for the visualization to fully populate.
- The included `anydesk` file is an ARM64 Linux executable and may only run on compatible Linux ARM64 systems.

## License

No license has been specified yet. Add a license file before distributing or reusing this project publicly.

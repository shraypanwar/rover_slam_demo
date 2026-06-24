# ROS2 Jazzy Rover SLAM + Nav2 Autonomous Navigation

A custom differential drive rover built from scratch with URDF, capable of autonomous SLAM mapping and Nav2 point-to-point navigation in Gazebo Harmonic simulation.

## Demo
![SLAM Map Generation](docs/map_generation.png)
![Nav2 using 2D Goal Pose](docs/nav2_using_2DGoalPose.png)
![Nav2 using Terminal](docs/nav2_using_terminal.png)
![RViz Visualization](docs/Rviz.png)

## Tech Stack
- Ubuntu 24.04 + ROS2 Jazzy + Gazebo Harmonic
- Custom URDF rover (differential drive + 360 LiDAR)
- slam_toolbox for live occupancy map building
- Nav2 for autonomous point-to-point navigation
- ros_gz_bridge for Gazebo-ROS2 communication

## Project Structure
rover_slam_demo/
- urdf/ — Custom rover robot definition
- worlds/ — Gazebo 3D world with obstacles
- launch/ — Startup scripts
- config/ — Bridge, SLAM and Nav2 settings
- rviz/ — RViz visualization config
- maps/ — Saved map files
- docs/ — Demo screenshots

## Key Technical Challenges Solved
1. Custom Gazebo-ROS2 TF bridge — DiffDrive plugin publishes to /model/rover/tf, not generic /tf
2. slam_toolbox base_frame fix — Default is base_footprint but custom URDF uses base_link
3. Sim time synchronization — All nodes require use_sim_time: true

## Setup — Run Once Only

Install Required Packages:
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-sim
sudo apt install -y ros-jazzy-robot-state-publisher ros-jazzy-slam-toolbox
sudo apt install -y ros-jazzy-nav2-bringup ros-jazzy-teleop-twist-keyboard
sudo apt install -y ros-jazzy-nav2-map-server ros-jazzy-nav2-amcl

Clone and Build:
mkdir -p ~/rover_ws/src
cd ~/rover_ws/src
git clone https://github.com/shraypanwar/rover_slam_demo.git
cd ~/rover_ws
colcon build --packages-select rover_slam_demo

## IMPORTANT — Run This in Every New Terminal
source /opt/ros/jazzy/setup.bash
source ~/rover_ws/install/setup.bash

## Part 1 — Build a Map (First Time Only)

Terminal 1 — Launch Simulation + SLAM + RViz:
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 launch rover_slam_demo rover_full.launch.py

Wait 20 seconds for Gazebo and RViz to open.

Terminal 2 — Drive the rover to build the map:
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

Teleop controls (click terminal first to focus it):
i = forward
, = backward
j = turn left
l = turn right
k = STOP
q/z = increase/decrease speed

Drive around the full world for 60 seconds. Watch the map build in RViz.

Terminal 3 — Save the map (while Terminal 1 is still running):
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 run nav2_map_server map_saver_cli -f ~/rover_ws/my_rover_map

## Part 2 — Autonomous Navigation

Terminal 1 — Launch Simulation + SLAM + RViz:
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 launch rover_slam_demo rover_full.launch.py

Wait 20 seconds.

Terminal 2 — Launch Nav2:
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 launch rover_slam_demo nav2_custom.launch.py

Wait until you see: lifecycle_manager_navigation: Managed nodes are active

Terminal 3 — Send autonomous navigation goal:
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.0, y: 1.0, z: 0.0}, orientation: {w: 1.0}}}}"

Expected result: Goal finished with status: SUCCEEDED

Alternative — Use RViz directly:
Click the 2D Goal Pose button in RViz toolbar, then click anywhere on the map.

## Verify Everything is Working

Check slam_toolbox frame (must return base_link):
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 param get /slam_toolbox base_frame

Check laser scan is publishing (should show 20Hz):
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 topic hz /scan

Check map is publishing:
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 topic hz /map

Check TF tree is healthy:
source /opt/ros/jazzy/setup.bash && source ~/rover_ws/install/setup.bash
ros2 run tf2_tools view_frames

## If Anything Breaks — Full Reset
pkill -9 -f gz
pkill -9 -f slam_toolbox
pkill -9 -f rviz2
pkill -9 -f parameter_bridge
pkill -9 -f robot_state_publisher
pkill -9 -f controller_server
pkill -9 -f planner_server
pkill -9 -f bt_navigator
pkill -9 -f behavior_server
pkill -9 -f lifecycle_manager

Wait 5 seconds, then start again from Terminal 1.

## Potential Improvements
- Frontier-based autonomous exploration instead of manual teleop
- Multi-goal waypoint navigation
- Add camera sensor for visual feedback
- Use saved map with AMCL localization without re-mapping
- 3D LiDAR for more detailed environment mapping

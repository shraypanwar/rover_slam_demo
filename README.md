# ROS2 Jazzy Rover SLAM + Nav2 Autonomous Navigation

A custom differential drive rover built from scratch with URDF, capable of autonomous SLAM mapping and Nav2 point-to-point navigation in Gazebo Harmonic simulation.

## Demo
![SLAM Map Generation](docs/map_generation.png)
![Nav2 using 2D Goal Pose](docs/nav2_using_2DGoalPose.png)
![Nav2 using Terminal](docs/nav2_using_terminal.png)
![RViz Visualization](docs/Rviz.png)

## Tech Stack
- Ubuntu 24.04 + ROS2 Jazzy + Gazebo Harmonic
- Custom URDF rover (differential drive + 360° LiDAR)
- slam_toolbox for live occupancy map building
- Nav2 for autonomous point-to-point navigation
- ros_gz_bridge for Gazebo-ROS2 communication

## Key Technical Challenges Solved
1. **Custom Gazebo-ROS2 TF bridge** — DiffDrive plugin publishes to `/model/rover/tf`, not generic `/tf`. Bridge config must explicitly map this.
2. **slam_toolbox base_frame fix** — Default is `base_footprint` but custom URDF uses `base_link`. Fixed via `slam_params.yaml`.
3. **Sim time synchronization** — All nodes require `use_sim_time: true` and slam_toolbox must be launched via `IncludeLaunchDescription`, not bare `Node`.

## How to Run

### Terminal 1 — Launch Simulation + SLAM
```bash
source /opt/ros/jazzy/setup.bash
source ~/rover_ws/install/setup.bash
ros2 launch rover_slam_demo rover_full.launch.py
```

### Terminal 2 — Launch Nav2
```bash
source /opt/ros/jazzy/setup.bash
source ~/rover_ws/install/setup.bash
ros2 launch rover_slam_demo nav2_custom.launch.py
```

### Terminal 3 — Send Autonomous Goal
```bash
source /opt/ros/jazzy/setup.bash
source ~/rover_ws/install/setup.bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
"{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.0, y: 1.0, z: 0.0}, orientation: {w: 1.0}}}}"
```

## Required Packages
```bash
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-sim
sudo apt install -y ros-jazzy-robot-state-publisher ros-jazzy-slam-toolbox
sudo apt install -y ros-jazzy-nav2-bringup ros-jazzy-teleop-twist-keyboard
sudo apt install -y ros-jazzy-nav2-map-server
```

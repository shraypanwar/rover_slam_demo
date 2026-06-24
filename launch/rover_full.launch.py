import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('rover_slam_demo')
    slam_toolbox_share = get_package_share_directory('slam_toolbox')

    urdf_path = os.path.join(pkg_share, 'urdf', 'rover.urdf')
    world_path = os.path.join(pkg_share, 'worlds', 'rover_world.sdf')
    bridge_config = os.path.join(pkg_share, 'config', 'bridge.yaml')
    rviz_config = os.path.join(pkg_share, 'rviz', 'rover_slam.rviz')

    with open(urdf_path, 'r') as f:
        robot_desc = f.read()

    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
        output='screen'
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'rover', '-topic', 'robot_description', '-z', '0.1'],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config, 'use_sim_time': True}],
        output='screen'
    )

    slam_toolbox = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(slam_toolbox_share, 'launch', 'online_async_launch.py')
                ),
                launch_arguments={
                    'use_sim_time': 'true',
                    'slam_params_file': os.path.join(pkg_share, 'config', 'slam_params.yaml')
                }.items()
            )
        ]
    )

    rviz = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                arguments=['-d', rviz_config],
                parameters=[{'use_sim_time': True}],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        bridge,
        slam_toolbox,
        rviz,
    ])

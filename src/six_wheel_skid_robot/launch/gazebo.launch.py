from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    pkg_name = 'six_wheel_skid_robot'
    pkg_share = get_package_share_directory(pkg_name)

    # Xacro file path
    xacro_file = os.path.join(pkg_share, 'urdf', 'new_robot.urdf.xacro')

    return LaunchDescription([
        # Launch Gazebo with empty world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
            ])
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'robot_description': Command(['xacro ', xacro_file])
            }]
        ),

        # Spawn robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'ugv',
                '-topic', 'robot_description',
                '-x', '0', '-y', '0', '-z', '0.2'
            ],
            output='screen'
        ),
    ])

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

import os

def generate_launch_description():
    urdf_file_path = PathJoinSubstitution([
        FindPackageShare('quadped_urdf'),
        'urdf',
        'quadped_URDF.urdf'
    ])

    return LaunchDescription([
        # Launch Ignition Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('ros_ign_gazebo'),
                    'launch',
                    'ign_gazebo.launch.py'
                ])
            ]),
            launch_arguments={
                'ign_args': '-r empty.sdf'
            }.items()
        ),

        # Publish robot_description from URDF (not Xacro)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command(['cat', urdf_file_path])
            }]
        ),

        # Spawn robot into Ignition Gazebo
        Node(
            package='ros_ign_gazebo',
            executable='create',
            output='screen',
            arguments=[
                '-name', 'my_robot',
                '-x', '0', '-y', '0', '-z', '0.5',
                '-topic', 'robot_description'
            ]
        )
    ])

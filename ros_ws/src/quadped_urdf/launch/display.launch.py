# quadped_urdf/launch/display.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory('quadped_urdf'),
        'urdf',
        'quadped_urdf.urdf'
    )

    rviz_config_file = os.path.join(
        get_package_share_directory('quadped_urdf'),
        'urdf.rviz'  # Or wherever your RViz config is
    )

    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()

    return LaunchDescription([
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description_content}]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        )
    ])

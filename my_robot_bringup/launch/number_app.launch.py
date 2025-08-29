from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    param_path = os.path.join(get_package_share_directory('my_robot_bringup'), 
                             'config', 'number_app.yaml')
    return LaunchDescription([
        Node(
            package='my_py_pkg',
            executable='number_publisher',
            name='number_publisher_node',
            remappings=[('/number', '/new_number')],
            # parameters=[{'number': 8, 'timer_interval': 2.0}]
            parameters=[param_path]

        ),
        Node(
            package="my_py_pkg",
            executable='number_counter',
            name='number_counter_node',
            remappings=[
                ('/number', '/new_number'),
            ('/number_counter', '/new_counter')
            ]

        )
    ])
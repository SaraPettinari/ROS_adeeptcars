from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='adeeptcar',
            executable='move',
        ),
        Node(
            package='adeeptcar',
            executable='ultrasonic',
        ),
        Node(
            package='adeeptcar',
            executable='led',
        ),
        Node(
            package='adeeptcar',
            executable='controller',
        )
    ])
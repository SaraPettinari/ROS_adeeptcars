from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='adeeptcar',
            executable='move',
            remappings=[
                ('/cmd_vel', 'pina/cmd_vel')]
        ),
        Node(
            package='adeeptcar',
            executable='ultrasonic',
            remappings=[
                ('/range', 'pina/range')]
        ),
        Node(
            package='adeeptcar',
            executable='led',
        ),
        Node(
            package='adeeptcar',
            executable='controller',
            remappings=[
                ('/cmd_vel', 'pina/cmd_vel'),
                ('/range', 'pina/range')
                ]
        ),
        Node(
            package='adeeptcar',
            executable='status',
            remappings=[
                ('/range', 'pina/range')]
        )
    ])
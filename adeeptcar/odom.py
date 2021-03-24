# #!/usr/bin/env python3
# import time
# import RPi.GPIO as GPIO
# import rclpy
# from rclpy.node import Node
# from nav_msgs.msg import Odometry
# from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

# odometry_position = Odometry()


# def setup():
#     print('--> ODOM node')
#     # initialization of ROS subscriber
#     rclpy.init()
#     node = rclpy.create_node('odometry')
#     node.create_subscription(Twist, '/cmd_vel', odom, 10)
#     odom_pub = node.create_publisher(Odometry, '/odom', 10)
#     current_time = node.get_clock().now()
#     last_time = node.get_clock().now()


# def position_extimation(positionXY):
#     if positionXY == 'parallel+y':
#         #
#     elif positionXY == 'parallel-y':
#         #
#     elif positionXY == 'parallel+x':
#         #
#     elif positionXY == 'parallel-x':
#         #


# def odom(twistMsg):
#     print('ciao')


# if __name__ == '__main__':
#     setup()

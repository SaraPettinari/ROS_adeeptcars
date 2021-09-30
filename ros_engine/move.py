# Gira o si muove

import rclpy
from geometry_msgs.msg import Twist
from .hardware.motors import Motors

motors = Motors()

def setup():  # Motor initialization
    print('--> MOTOR node')
    motors.motor_init()

    # initialization of ROS subscriber
    rclpy.init()
    node = rclpy.create_node('movement_actuator')
    node.create_subscription(Twist, '/cmd_vel', move, 10)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()
        print('Shutting down: stopping motors')
        motors.motor_stop()


# ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
def move(twistMsg, radius=0.6):   # 0 < radius <= 1
    turn = ''
    lin_vel = 0
    lin_vel_x = twistMsg.linear.x
    lin_vel_y = twistMsg.linear.y
    if lin_vel_x != 0 and lin_vel_y == 0:
        lin_vel = lin_vel_x
    elif lin_vel_x == 0 and lin_vel_y != 0:
        lin_vel = lin_vel_y
    ang_vel = twistMsg.angular.z
    if lin_vel < 0.8:
        speed = abs(0.8 * 100)
    else:
        speed = abs(lin_vel * 100)
    if lin_vel > 0:
        direction = 'forward'
    elif lin_vel < 0:
        direction = 'backward'
    else:
        direction = 'no'
    if ang_vel > 0:
        turn = 'right'
        lin_vel = 1.0
    elif ang_vel < 0:
        turn = 'left'
        lin_vel = 1.0
    if direction == 'forward':
        if turn == 'right':
            motors.motor_left(0, motors.left_backward, int(speed*radius))
            motors.motor_right(1, motors.right_forward, speed)
        elif turn == 'left':
            motors.motor_left(1, motors.left_forward, speed)
            motors.motor_right(0, motors.right_backward, int(speed*radius))
        else:
            motors.motor_left(1, motors.left_forward, speed)
            motors.motor_right(1, motors.right_forward, speed)
    elif direction == 'backward':
        if turn == 'right':
            motors.motor_left(0, motors.left_forward, int(speed*radius))
            motors.motor_right(1, motors.right_backward, speed)
        elif turn == 'left':
            motors.motor_left(1, motors.left_backward, speed)
            motors.motor_right(0, motors.right_forward, int(speed*radius))
        else:
            motors.motor_left(1, motors.left_backward, speed)
            motors.motor_right(1, motors.right_backward, speed)
    elif direction == 'no':
        if turn == 'right':
            motors.motor_left(1, motors.left_backward, speed)
            motors.motor_right(1, motors.right_forward, speed)
        elif turn == 'left':
            motors.motor_left(1, motors.left_forward, speed)
            motors.motor_right(1, motors.right_backward, speed)
        else:
            motors.motor_stop()
    else:
        pass


if __name__ == '__main__':
    setup()

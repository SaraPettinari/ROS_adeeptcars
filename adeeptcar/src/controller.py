#!/usr/bin/env python3
import time
import rclpy
from std_msgs.msg import ColorRGBA
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range

velocity = Twist()
led = ColorRGBA()

def setup():
    print('--> CONTROLLER node')
    # node initialization
    rclpy.init()
    node = rclpy.create_node('controller')
    node.create_subscription(Range, '/range', movementController, 10)
    velocity_pub = node.create_publisher(Twist, '/cmd_vel', 10)
    led_pub = node.create_publisher(ColorRGBA, '/led_RGB', 10)
    
    def timer_callback():
        #publish on cmd_vel topic
        #node.get_logger().info('Publishing: "%s"' % velocity.linear.x % velocity.angular.z)
        velocity_pub.publish(velocity)
        #publish on led_RGB topic
        #node.get_logger().info('Publishing: "%s"' % led.r % led.g % led.b)
        led_pub.publish(led)
    
    timer_period = 0.5  # seconds
    timer = node.create_timer(timer_period, timer_callback)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()


def movementController(distance):
    RED = 0.0
    GREEN = 0.0
    BLUE = 0.0
    velocity.linear.x = 0.8
    velocity.angular.z = 0.0
     # rotazione
    if distance.range >= 0.2 and distance.range < 0.4:
        velocity.angular.z = 1.0
        rotation(velocity.linear.x, velocity.angular.z)
        print('Rotateeee')
    # decelera
    elif distance.range >= 0.4 and distance.range < 0.6:
        velocity.linear.x = velocity.linear.x / 2
    # retromarcia
    elif distance.range >= 0.04 and distance.range < 0.2:
        velocity.linear.x = - velocity.linear.x
        velocity.angular.z = - 0.6
        rotation(velocity.linear.x, velocity.angular.z)
        print('RETROMARCIA!!!')
    # normale
    elif distance.range >= 0.6 and distance.range < 4.0:
        GREEN = 0.5
        BLUE = 0.5
    else:
        print('The car crashed! --> ' + str(distance.range))
        RED = 1.0
        velocity.linear.x = - velocity.linear.x
        rotation(velocity.linear.x, 0.5)
    changeLedColor(RED, GREEN, BLUE)
    print(distance.range)

def rotation(linear, angular):
    velocity.linear.x = linear
    velocity.angular.z = angular
    time.sleep(0.2)

def changeLedColor(red, green, blue):
    led.r = red
    led.g = green
    led.b = blue

if __name__ == '__main__':
	setup()
# Sott ai dati degli ultrasuoni
# Pub cmd_vel in tondo
# Pub ON-OFF led
# (forse) Sott Tracking line

import threading
import rclpy
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
from std_msgs.msg import ColorRGBA

led = True


def getDistance(r: Range):
    print(str(r.range))


def setup():
    rclpy.init()
    node = rclpy.create_node('controller')
    velocity_pub = node.create_publisher(Twist, '/cmd_vel', 10)
    led_pub = node.create_publisher(ColorRGBA, '/led', 10)
    range_sub = node.create_subscription(Range, '/range', getDistance, 10)

    def vel_callback():
        vel = Twist()
        vel.linear.x = 0.5
        vel.angular.z = 1.0
        velocity_pub.publish(vel)

    def led_callback():
        global led
        color = ColorRGBA()
        if led:
            color.r = 1.0
        else:
            color.r = 0.0
        led = not led

        led_pub.publish(color)

    timer_period = 0.5  # seconds
    timer1 = node.create_timer(timer_period, vel_callback)
    timer2 = node.create_timer(timer_period, led_callback)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_timer(timer1)
        node.destroy_timer(timer2)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    setup()

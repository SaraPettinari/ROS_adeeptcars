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

rclpy.init()
node = rclpy.create_node('controller')


def velocity_thread():
    velocity_pub = node.create_publisher(Twist, '/cmd_vel', 10)
    node.get_logger().info('stampa C')

  #  rclpy.spin(node)
    vel = Twist()
    vel.linear.x = 0.5
    vel.angular.z = 1.0
    velocity_pub.publish(vel)


def led_thread():
    led_pub = node.create_publisher(ColorRGBA, '/led', 10)
    node.get_logger().info('stampa L')
 #   rclpy.spin(node)
    global led
    color = ColorRGBA()
    if led:
        color.r = 1.0
    else:
        color.r = 0.0
    led = not led

    led_pub.publish(color)


def range_thread():
    range_sub = node.create_subscription(Range, '/range', getDistance, 10)
    node.get_logger().info('stampa R')
   # rclpy.spin(node)


def getDistance(r: Range):
    print(str(r.range))


def setup():
    thread3 = threading.Thread(target=range_thread())
    thread2 = threading.Thread(target=velocity_thread())
    thread1 = threading.Thread(target=led_thread())
    thread3.start()
    thread2.start()
    thread1.start()
    
    for i in range(100):
        thread3.join()
        thread2.join()
        thread1.join()

    rclpy.spin(node)


if __name__ == '__main__':
    setup()

import time
import RPi.GPIO as GPIO
import rclpy
from std_msgs.msg import String
from sensor_msgs.msg import Range


status = String()

def setup():
    print('--> STATUS node')
    rclpy.init()
    node = rclpy.create_node('status_node')
    status_pub = node.create_publisher(String, '/status', 10)
    node.create_subscription(Range, '/range', status_output, 10)

    def timer_callback():  # definition of a timer function that manages all the publications
        node.get_logger().info('Publishing: "%s"' % status)
        status_pub.publish(status)

    timer_period = 0.5  # seconds
    timer = node.create_timer(timer_period, timer_callback)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()


def status_output(distance):
    status.data = 'OK'
    if distance.range < 0.4:
        status.data = 'DANGER'


if __name__ == '__main__':
    setup()

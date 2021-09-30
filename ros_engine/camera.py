import rclpy
from sensor_msgs.msg import Image
from picamera import PiCamera

camera = PiCamera()

def setup():
    print('--> ULTRASONIC node')
    rclpy.init()
    node = rclpy.create_node('ultrasonic_sensor')
    image_pub = node.create_publisher(Image, '/img', 10)

    image_data = Image()

    def timer_callback():  # definition of a timer function that manages all the publications
        dist = checkdist()
        print(dist)
        distance_data.range = dist
        node.get_logger().info('Publishing: "%s"' % distance_data.range)
        distance_pub.publish(distance_data)

    timer_period = 0.5  # seconds
    timer = node.create_timer(timer_period, timer_callback)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()


def get_image():
    camera

if __name__ == '__main__':
    setup()

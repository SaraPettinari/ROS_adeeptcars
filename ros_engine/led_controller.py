# Sub -> cambia status del led

import rclpy
from std_msgs.msg import ColorRGBA
from .hardware.led_strip import LedStrip

led = LedStrip()


def setup():
    print('--> LED node')
    rclpy.init()
    node = rclpy.create_node('led_actuator')
    node.create_subscription(ColorRGBA, '/led', manageLed, 10)

    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()
        print('Shutting down: stopping LEDs')


def manageLed(colorMsg):
    R = colorMsg.r
    G = colorMsg.g
    B = colorMsg.b

    led.set_color(R, G, B)


if __name__ == '__main__':
    setup()

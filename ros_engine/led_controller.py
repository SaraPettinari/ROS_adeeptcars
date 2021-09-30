# Sub -> cambia status del led

import pathlib
import os
import rclpy
from std_msgs.msg import ColorRGBA


# Get current working path
path = str(pathlib.Path(__file__).parent.absolute())



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

    cmd = 'python3 ' + path + '/hardware/led_strip.py ' + \
        str(R) + ' ' + str(G) + ' ' + str(B)
    print(path)
    os.popen("sudo -S %s" % (cmd), 'w')


if __name__ == '__main__':
    setup()

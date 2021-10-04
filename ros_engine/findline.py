import rclpy
from std_msgs.msg import Bool
from .hardware.tracking_sensor import TrackingSensor

track_sensor = TrackingSensor()

def setup():
    print('--> LINE node')

    rclpy.init()
    node = rclpy.create_node('findline_sensor')
    line_pub = node.create_publisher(Bool, '/line_found', 10)
    
    line = Bool()
    
    def timer_callback():
        line.data = track_sensor.run()
        line_pub.publish(line)
    
    timer_period = 0.5  # seconds
    timer = node.create_timer(timer_period, timer_callback)
    
    rclpy.spin(node)

    if KeyboardInterrupt:
        node.destroy_timer(timer)
        node.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    setup()

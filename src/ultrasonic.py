#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import rclpy
from std_msgs.msg import Float32

#TRIG IO port
TrigPin = 11  # Pin number of input terminal of ultrasonic module
#ECHO IO port
EchoPin = 8 # Pin number of output terminal of ultrasonic module

dist = 0

# S = (T2 - T1) * Vs/2
def checkdist():       #Reading distance
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TrigPin, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(EchoPin, GPIO.IN)
    GPIO.output(TrigPin, GPIO.HIGH) # Set the input end of the module to high level and emit an initial sound wave
    time.sleep(0.000015)
    GPIO.output(TrigPin, GPIO.LOW)
    while not GPIO.input(EchoPin): # When the module no longer receives the initial sound wave
        pass
    t1 = time.time() # T1 -> time when the initial sound wave is emitted
    while GPIO.input(EchoPin): # When the module receives the return sound wave
        pass
    t2 = time.time() # T2 -> time when the return sound wave is captured
    distance = (t2-t1)*340/2
    return distance


if __name__ == '__main__':
	print('--> ULTRASONIC node')
	rclpy.init()
	node = rclpy.create_node('ultrasonic_sensor')
	distance_pub = rclpy.create_publisher(Float32, '/ultrasonic', 10)
	rate = rclpy.create_rate(10)
	control = True
	try:
		while not rclpy.shutdown():
			dist = checkdist()
			distance_pub.publish(dist)
			rate.sleep()
	except KeyboardInterrupt:
		control = False
		exit()

print('Shutting down: stopping ultrasonic sensor')
GPIO.cleanup()
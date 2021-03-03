#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import sys
import rclpy
from std_msgs.msg import ColorRGBA
import os
import subprocess
import pathlib


lightMode = 'none'		#'none' 'police' 'breath'

#Get current working path
path = str(pathlib.Path(__file__).parent.absolute())
#print(path)

def setup():
	print('--> LED node')

def manageLed(colorMsg):
	R = colorMsg.r
	G = colorMsg.g
	B = colorMsg.b
	
	cmd = 'python3 ' + path + '/led_strip.py ' + str(R) + ' ' + str(G) + ' ' + str(B)
	os.popen("sudo -S %s"%(cmd), 'w')

if __name__ == '__main__':
	try:
		setup()
	except KeyboardInterrupt:
		exit()

rclpy.init()
node = rclpy.create_node('led_actuator')
node.create_subscription(ColorRGBA, '/led_RGB', manageLed, 10)

rclpy.spin(node)
	
print('Shutting down: stopping LEDs')
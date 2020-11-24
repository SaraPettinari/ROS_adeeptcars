#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import sys
import rospy
from std_msgs.msg import ColorRGBA
import os
import subprocess
import pathlib


# LED_COUNT = 16	  # Number of LED pixels.
# LED_PIN = 12	  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA	= 10	  # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 255	 # Set to 0 for darkest and 255 for brightest
# LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL	= 0	   # set to '1' for GPIOs 13, 19, 41, 45 or 53

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
	
	cmd = 'python3 ' + path + '/script/led_script.py ' + str(R) + ' ' + str(G) + ' ' + str(B)
	os.popen("sudo -S %s"%(cmd), 'w')

if __name__ == '__main__':
	try:
		setup()
	except KeyboardInterrupt:
		exit()
	
rospy.init_node('led_actuator')
rospy.Subscriber('/light_controller', ColorRGBA, manageLed)

rospy.spin()
print('Shutting down: stopping LEDs')

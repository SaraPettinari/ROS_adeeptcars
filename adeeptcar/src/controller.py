#!/usr/bin/env python3
import time
import rospy
from std_msgs.msg import Float32, ColorRGBA
from geometry_msgs.msg import Twist

rospy.init_node('controller')
velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
colorled_pub = rospy.Publisher('/light_controller', ColorRGBA, queue_size=3)

RED = 0.0
GREEN = 0.0
BLUE = 0.0

def setup():
    print('--> CONTROLLER node')
 #   rate = rospy.Rate(10)  # 10hz

def changeLedColor(red, green, blue):
    led = ColorRGBA()
    led.r = red
    led.g = green
    led.b = blue
    colorled_pub.publish(led)

def rotation(linear, angular):
    cmd_velocity = Twist()
    cmd_velocity.linear.x = linear
    cmd_velocity.angular.z = angular
 #   velocity_pub.publish(cmd_velocity)
    time.sleep(0.2)

# ultrasonic working range: 2 cm - 4 m
def movementController(distance):
    tempR = RED
    tempG = GREEN
    tempB = BLUE
    cmd_velocity = Twist()
    cmd_velocity.linear.x = 0.8
    cmd_velocity.angular.z = 0.0
    #rotazione
    if distance.data >= 0.2 and distance.data < 0.4:
        cmd_velocity.angular.z = 1.0
        rotation(cmd_velocity.linear.x, cmd_velocity.angular.z)
        print('Rotateeee')
    #    changeLedColor(1.0, 1.0, 0.0)
    #decelera
    elif distance.data >= 0.4 and distance.data < 0.6:
        cmd_velocity.linear.x = cmd_velocity.linear.x / 2
    #retromarcia
    elif distance.data >= 0.04 and distance.data < 0.2:
        cmd_velocity.linear.x = - cmd_velocity.linear.x
        cmd_velocity.angular.z = - 0.6
        rotation(cmd_velocity.linear.x, cmd_velocity.angular.z)
        tempR = 0.5
        tempG = 0.5
        tempB = 0.0
        print('RETROMARCIA!!!')
    #normale
    elif distance.data >= 0.6 and distance.data < 4.0:
        tempR = 0.0
        tempG = 0.5
        tempB = 0.5
    else:
        print('The car crashed! --> ' + str(distance.data))
        tempR = 1.0
        tempG = 0.0
        tempB = 0.0
        cmd_velocity.linear.x = - cmd_velocity.linear.x
        rotation(cmd_velocity.linear.x, 0.5)
    if RED != tempR or GREEN != tempG or BLUE != tempB:
        changeGlobalVar(tempR, tempG, tempB)
        changeLedColor(RED, GREEN, BLUE)
    print(distance.data)
    print('Velocity: ' + str(cmd_velocity.linear.x) + ' - ' + str(cmd_velocity.angular.z))
    velocity_pub.publish(cmd_velocity)

def changeGlobalVar(r, g, b):
    global RED
    global GREEN
    global BLUE

    RED = r
    GREEN = g
    BLUE = b

if __name__ == '__main__':
    try:
        setup()
    except KeyboardInterrupt:
        exit()

rospy.Subscriber('/ultrasonic', Float32, movementController)
rospy.spin()
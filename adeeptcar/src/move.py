#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 26
Motor_A_Pin2  = 21
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 1
Dir_backward  = 0

left_forward  = 1
left_backward = 0

right_forward = 0
right_backward= 1

pwn_A = 0
pwm_B = 0

def motorStop():#Motor stops
	GPIO.output(Motor_A_Pin1, GPIO.LOW)
	GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_B_Pin1, GPIO.LOW)
	GPIO.output(Motor_B_Pin2, GPIO.LOW)
	GPIO.output(Motor_A_EN, GPIO.LOW)
	GPIO.output(Motor_B_EN, GPIO.LOW)


def setup():#Motor initialization
	print('--> MOTOR node')
	global pwm_A, pwm_B
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Motor_A_EN, GPIO.OUT)
	GPIO.setup(Motor_B_EN, GPIO.OUT)
	GPIO.setup(Motor_A_Pin1, GPIO.OUT)
	GPIO.setup(Motor_A_Pin2, GPIO.OUT)
	GPIO.setup(Motor_B_Pin1, GPIO.OUT)
	GPIO.setup(Motor_B_Pin2, GPIO.OUT)

	motorStop()
	try:
		pwm_A = GPIO.PWM(Motor_A_EN, 1000)
		pwm_B = GPIO.PWM(Motor_B_EN, 1000)
	except:
		pass

	# initialization of ROS subscriber
	rclpy.init()
	node = rclpy.create_node('movement_actuator')
	node.create_subscription(Twist, '/cmd_vel', move, 10)

	rclpy.spin(node)
	
	if KeyboardInterrupt:
		node.destroy_node()
		rclpy.shutdown()
		print('Shutting down: stopping motors')
		motorStop()
		GPIO.cleanup()


def motor_left(status, direction, speed):#Motor 2 positive and negative rotation
	if speed > 100: #to avoid problems with duty cycle
		speed = 100
	if status == 0: # stop
		GPIO.output(Motor_B_Pin1, GPIO.LOW)
		GPIO.output(Motor_B_Pin2, GPIO.LOW)
		GPIO.output(Motor_B_EN, GPIO.LOW)
	else:
		if direction == Dir_backward:
			GPIO.output(Motor_B_Pin1, GPIO.HIGH)
			GPIO.output(Motor_B_Pin2, GPIO.LOW)
			pwm_B.start(100)
			pwm_B.ChangeDutyCycle(speed)
		elif direction == Dir_forward:
			GPIO.output(Motor_B_Pin1, GPIO.LOW)
			GPIO.output(Motor_B_Pin2, GPIO.HIGH)
			pwm_B.start(0)
			pwm_B.ChangeDutyCycle(speed)


def motor_right(status, direction, speed):#Motor 1 positive and negative rotation
	if speed > 100: #to avoid problems with duty cycle
		speed = 100
	if status == 0: # stop
		GPIO.output(Motor_A_Pin1, GPIO.LOW)
		GPIO.output(Motor_A_Pin2, GPIO.LOW)
		GPIO.output(Motor_A_EN, GPIO.LOW)
	else:
		if direction == Dir_forward:#
			GPIO.output(Motor_A_Pin1, GPIO.HIGH)
			GPIO.output(Motor_A_Pin2, GPIO.LOW)
			pwm_A.start(100)
			pwm_A.ChangeDutyCycle(speed)
		elif direction == Dir_backward:
			GPIO.output(Motor_A_Pin1, GPIO.LOW)
			GPIO.output(Motor_A_Pin2, GPIO.HIGH)
			pwm_A.start(0)
			pwm_A.ChangeDutyCycle(speed)
	return direction

# ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
def move(twistMsg, radius=0.6):   # 0 < radius <= 1  
	turn = ''
	lin_vel = 0
	lin_vel_x = twistMsg.linear.x
	lin_vel_y = twistMsg.linear.y
	if lin_vel_x != 0 and lin_vel_y == 0:
		lin_vel = lin_vel_x
	elif lin_vel_x == 0 and lin_vel_y != 0:
		lin_vel = lin_vel_y
	ang_vel = twistMsg.angular.z
	if lin_vel < 0.8:
		speed = abs(0.8 * 100)
	else:
		speed = abs(lin_vel * 100)
	if lin_vel > 0:
		direction = 'forward'
	elif lin_vel < 0:
		direction = 'backward'
	else:
		direction = 'no'
	if ang_vel > 0:
		turn = 'right'
		lin_vel = 1.0
	elif ang_vel < 0:
		turn = 'left'
		lin_vel = 1.0
	if direction == 'forward':
		if turn == 'right':
			motor_left(0, left_backward, int(speed*radius))
			motor_right(1, right_forward, speed)
		elif turn == 'left':
			motor_left(1, left_forward, speed)
			motor_right(0, right_backward, int(speed*radius))
		else:
			motor_left(1, left_forward, speed)
			motor_right(1, right_forward, speed)
	elif direction == 'backward':
		if turn == 'right':
			motor_left(0, left_forward, int(speed*radius))
			motor_right(1, right_backward, speed)
		elif turn == 'left':
			motor_left(1, left_backward, speed)
			motor_right(0, right_forward, int(speed*radius))
		else:
			motor_left(1, left_backward, speed)
			motor_right(1, right_backward, speed)
	elif direction == 'no':
		if turn == 'right':
			motor_left(1, left_backward, speed)
			motor_right(1, right_forward, speed)
		elif turn == 'left':
			motor_left(1, left_forward, speed)
			motor_right(1, right_backward, speed)
		else:
			motorStop()
	else:
		pass




def destroy():
	motorStop()
	GPIO.cleanup()             # Release resource


if __name__ == '__main__':
	setup()

#setup()

#!/usr/bin/env python

import rospy
import time
import math
import cv2
from Drive import Drive
from sensor_msgs.msg import LaserScan

orientation = 0
distance = 0.4
forward_distance = 0

def callback(data):
	global orientation, distance, forward_distance
	average = sum(data.ranges[520:561])/40
	forward_distance = average
	A = data.ranges[60]
	B = data.ranges[300]
	c = math.radians(60)
	C = math.sqrt(A*A + B*B - 2*A*B*math.cos(c))
	b = math.acos(-(B*B - C*C - A*A)/(2*A*C))
	h = A * math.sin(b)
	d = data.ranges[180]
	distance = h
	value = h/d
	if value > 1:
		orientation = 0
	else:
		orientation = math.degrees(math.acos(value))

	if A > B:
		orientation *= -1

def follow_wall():
	rospy.init_node("topic")
	scanSubscriber = rospy.Subscriber("/scan", LaserScan, callback)
	while not rospy.is_shutdown():
		if forward_distance < 1.1:
			print(forward_distance)
			steering_angle = 30
		else:
			steering_angle = 4 * (0.4 - distance) + 2 * (0 - orientation)
			print("Distance " + str(distance) + " Orientation " + str(orientation) + " Steering  " + str(steering_angle))
		Drive.send_drive_signal(speed=0.2, time=0.1, steering_angle=steering_angle, use_safety_controller=True)
	
if __name__ == '__main__':
	follow_wall()
		




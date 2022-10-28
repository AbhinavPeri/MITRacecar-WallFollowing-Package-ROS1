#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from Wall_Following.msg import safety_message
from nav_msgs.msg import Odometry

brake = False
velocity = 0
safetyPublisher = rospy.Publisher("/safety", safety_message, queue_size=1)

def callback(data):
	global brake
	lookahead = 1.4*velocity
	if lookahead > 0.55:
		lookahead = 0.55
	value = False
	print(lookahead)
	for i in range(360, 721):
		if data.ranges[i] < lookahead:
			value = True
	brake = value
	
def callback2(data):
	global velocity
	velocity = data.twist.twist.linear.x

def safety_controller():
	rospy.init_node("safety_sloth")
        laserSubscriber = rospy.Subscriber("/scan", LaserScan, callback)
	odometrySubscriber = rospy.Subscriber("/odom", Odometry, callback2)
	while not rospy.is_shutdown():
		msg = safety_message()
        	msg.brake = brake
        	safetyPublisher.publish(msg)

if __name__ == '__main__':
	safety_controller()

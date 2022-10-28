#/usr/bin/env python

import rospy
import time
from Wall_Following.msg import safety_message
from ackermann_msgs.msg import AckermannDriveStamped
from Timer import Timer


class Drive:
	

	stop = False
	
	def callback(data):
		global stop
		stop = data.brake

	safety_subscriber = rospy.Subscriber("/safety", safety_message, callback)
	drive_pub = rospy.Publisher("ackermann_cmd", AckermannDriveStamped, queue_size=1)
	global drive_pub
	@staticmethod
	def send_drive_signal(steering_angle, speed, time, acceleration=0, jerk=0, steering_angle_velocity=0, use_safety_controller=True):
		rate = rospy.Rate(10)
		timer = Timer()
		timer.reset()
        	while not rospy.is_shutdown() and timer.get_elapsed_time() < time:
                	if stop and use_safety_controller:
				while stop:
					pass
			msg = AckermannDriveStamped()
                	msg.drive.speed = speed
			msg.drive.steering_angle = steering_angle
			msg.drive.acceleration = acceleration
			msg.drive.jerk = jerk
			msg.drive.steering_angle_velocity
                	drive_pub.publish(msg)
                rate.sleep()

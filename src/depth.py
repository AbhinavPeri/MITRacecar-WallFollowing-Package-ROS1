#!/usr/bin/env python

import rospy
import cv2
import math
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

depth_image = Image()

def callback(data):
	global depth_image
	depth_image = data

def process_image():
	rospy.init_node("Image_processor")
	cv2.namedWindow("Original")
	depth_subscriber = rospy.Subscriber("/zed/depth/depth_registered", Image, callback)
	image_publisher = rospy.Publisher("/image_viewer", Image, queue_size=1)
	bridge = CvBridge()
	while not rospy.is_shutdown():
		try:
			image = bridge.imgmsg_to_cv2(depth_image, desired_encoding="32FC1")
			mask = np.array(image==10, dtype=np.ubyte)
			print(mask.shape)
			k = cv2.waitKey(1)
			if k == 27:
				cv2.destroyAllWindows()
			else:
				cv2.imshow("Original", image)
			#image_publisher.publish(bridge.cv2_to_imgmsg(mask, "8UC1"))
		except CvBridgeError as e:
			print(e)
if __name__ == '__main__':
	process_image()

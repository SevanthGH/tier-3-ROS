#!/usr/bin/python

import rospy
rospy.init_node('first_node')

rate = rospy.Rate(2) # We create a rate object of 2Hz

while not rospy.is_shutdown(): # Endless loop until Ctrl + C

	print "this is my first node"
	rate.sleep() # We sleep the needed time to maintain the rate


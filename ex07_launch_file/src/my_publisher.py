#! /usr/bin/env python

import rospy
import math
from goal_publisher.msg import PointArray

def callback(msg):
    for i in range (len(msg.goals)):
        print 'Point %i: x: %0.1f, y: %0.1f, z: %0.1f' %(i, msg.goals[i].x, msg.goals[i].y, msg.goals[i].z)

rospy.init_node('vel_launch_subscriber')
rospy.Subscriber('/points', PointArray, callback)
rospy.spin()


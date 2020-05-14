#! /usr/bin/env python

import rospy
import math
from goal_publisher.msg import PointArray

def callback(msg):
    #a = len(msg.goals)
    for i in range (len(msg.goals)):
        print 'point',i,': x: ',msg.goals[i].x, ', y: ',msg.goals[i].y, ', z: ', msg.goals[i].z

rospy.init_node('vel_launch_subscriber')
rospy.Subscriber('/points', PointArray, callback)
rospy.spin()


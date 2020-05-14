#! /usr/bin/env python

import rospy
import actionlib
from actionlib_tutorials.msg import FibonacciAction, FibonacciGoal, FibonacciFeedback, FibonacciResult

def callback(goal):
    r = rospy.Rate(2)
    success = True

    feedback.sequence = []
    #feedback.sequence.append(0)
    feedback.sequence.append(1)

    rospy.loginfo('%s: Executing, creating fibonacci sequence of order %i with seeds %i' % (action_server_name, goal.order, feedback.sequence[0])) #, feedback.sequence[1]))

    for i in range(goal.order):
        if action_server.is_preempt_requested():
            rospy.loginfo('%s: Preempted' % action_server_name)
            action_server.set_preempted()
            success = False
            break
        feedback.sequence.append(feedback.sequence[i] * 2)
        action_server.publish_feedback(feedback)
        r.sleep()

    if success:
        result.sequence = feedback.sequence
        rospy.loginfo('%s: Succeeded' % action_server_name)
        action_server.set_succeeded(result)

rospy.init_node('GP')
action_server = actionlib.SimpleActionServer("GP_server", FibonacciAction, callback, auto_start = False)
action_server_name = "GP Action Server"
action_server.start()

feedback = FibonacciFeedback()
result = FibonacciResult()

rospy.spin()

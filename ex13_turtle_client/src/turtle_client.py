#! /usr/bin/env python

import rospy
import actionlib
import time
from geometry_msgs.msg import Twist
from ex12_turtle_as.msg import MoveAction, MoveGoal, MoveFeedback, MoveResult

def callback(feedback):
    print('Feedback received: ')
    print(feedback)

rospy.init_node('turtle_action_client')

client = actionlib.SimpleActionClient('/moverobot_server', MoveAction)
client.wait_for_server()

goal = MoveGoal()
goal.direction = 'FORWARD'
goal.duration = 20

client.send_goal(goal, feedback_cb = callback)

rospy.sleep(5)
client.cancel_goal()

client.wait_for_result()
state_result = client.get_state()

print('[Result] State: %d' %state_result)

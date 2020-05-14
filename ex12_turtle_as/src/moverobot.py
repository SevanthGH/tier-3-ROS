#! /usr/bin/env python

import rospy
import actionlib
import time
from geometry_msgs.msg import Twist
from ex12_turtle_as.msg import MoveAction, MoveGoal, MoveFeedback, MoveResult

def callback(goal):
    r = rospy.Rate(2)
    success = True
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    count = Twist()
    time_stamp = rospy.get_time()
    print time_stamp

    if goal.direction == 'FORWARD' or goal.direction == 'BACKWARD':
        rospy.loginfo('%s: Turtlebot will move %s for the duration of %i seconds' % (action_server_name, goal.direction, goal.duration))#
        time_duration = 0
        while time_duration < goal.duration:
            time_duration = rospy.get_time() - time_stamp
            if (time_duration < goal.duration):
                if action_server.is_preempt_requested():
                    rospy.loginfo('%s: Preempted' % action_server_name)
                    action_server.set_preempted()
                    success = False
                    break
                if goal.direction == 'FORWARD':
                    count.linear.x = 0.3
                    feedback.current_state = "Moving forward!"
                    action_server.publish_feedback(feedback)
                if goal.direction == 'BACKWARD':
                    count.linear.x = -0.3
                    feedback.current_state = "Moving forward!"
                    action_server.publish_feedback(feedback)
            else:
                count.linear.x = 0
                feedback.current_state = "Finished moving!"
                action_server.publish_feedback(feedback)

            pub.publish(count)
            r.sleep()

    else:
        rospy.loginfo('%s: Incorrect goal: Please specify FORWARD or BACKWARD!' % action_server_name)

    if success:
        result.final_state = feedback.current_state
        rospy.loginfo('%s: Succeeded' % action_server_name)
        action_server.set_succeeded(result)

rospy.init_node('moverobot')
action_server = actionlib.SimpleActionServer("moverobot_server", MoveAction, callback, auto_start = False)
action_server_name = "moverobot Action Server"
action_server.start()

feedback = MoveFeedback()
result = MoveResult()

rospy.spin()

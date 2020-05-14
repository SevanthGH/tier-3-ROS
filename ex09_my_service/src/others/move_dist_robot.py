#! /usr/bin/env python
import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python class
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
import math
from tf.transformations import euler_from_quaternion

x = y = z = angle = 0
Flag = True
Flag1 = True
Flag2 = True
def position_robot(msg):
    global angle, x, y, z
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    quatern = ([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
    euler = euler_from_quaternion(quatern)
    angle = euler[2]

odom_sub = rospy.Subscriber('/odom', Odometry, position_robot)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


def move_forward():
        count.linear.x = 0.3
        count.angular.z = 0.0

def turn_left():
        count.linear.x = 0.0
        count.angular.z = math.radians(45)

def stop():
    count.linear.x = 0.0
    count.angular.z = 0.0

def my_callback(request):
    global count
    print "moving robot"
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(5)
    count = Twist()

    while not rospy.is_shutdown():
        for a in range(0,50):
            count.linear.x = 0.3
            count.angular.z = 0.0
            pub.publish(count)
            rate.sleep()
        #pub.publish(count)
        print 1

        for b in range(0,25):
            count.linear.x = 0.0
            count.angular.z = 0.3
            pub.publish(count)
            rate.sleep()
        print 2
    #rate.sleep()
    return EmptyResponse() # the service Response class, in this case EmptyResponse

#odom_sub = rospy.Subscriber('/odom', Odometry) #, position_robot)

rospy.init_node('service_move_dist_robot')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
my_service = rospy.Service('/my_service', Empty , my_callback) # create the Service
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.spin() # mantain the service open.

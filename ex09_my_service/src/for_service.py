#! /usr/bin/env python
import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python class
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
import math
from tf.transformations import euler_from_quaternion

x1 = y1 = x = y = angle = 0
angle_of_rotation = 90

def position_robot(msg):
    global angle, x, y, z
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    quatern = ([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
    euler = euler_from_quaternion(quatern)
    angle = euler[2]
    z = angle


odom_sub = rospy.Subscriber('/odom', Odometry, position_robot)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


def move_forward():
        count.linear.x = 0.1
        count.angular.z = 0.0

def turn_left():
        count.linear.x = 0.0
        count.angular.z = 0.1

def stop():
    count.linear.x = 0.0
    count.angular.z = 0.0

def EU_distance(x,y,x1,y1):
    return math.sqrt((x1-x)**2 + (y1-y)**2)

def update_distance():
    global x1, y1, angle, initial_angle, angle_of_rotation, z
    x1 = x
    y1 = y
    angle_of_rotation = angle_of_rotation + 90
    if angle_of_rotation > 360:
        angle_of_rotation = 90
        z = angle


def my_callback(request):
    global count, x1, y1, angle, initial_angle, angle_of_rotation, z
    print "moving robot"
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(100)
    count = Twist()
    c = 0
    sum = 0
    angle_of_rotation = 90

    while not rospy.is_shutdown():
        if EU_distance(x,y,x1,y1) < 1 and c%2 == 0:
            move_forward()
        elif EU_distance(x,y,x1,y1) > 1:
            turn_left()
            if angle <= 0 and c != 8:
                z = math.pi + (math.pi - abs(angle))
            if (math.degrees(abs(z))) >= angle_of_rotation or abs(z) > 6.28:
                stop()
                c = c + 2
                update_distance()
            if c == 10:
                sum = sum + 1
                print sum
                c = 2


        rate.sleep()
        pub.publish(count)
    return EmptyResponse() # the service Response class, in this case EmptyResponse

#odom_sub = rospy.Subscriber('/odom', Odometry) #, position_robot)

rospy.init_node('service_move_dist_robot')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
my_service = rospy.Service('/my_service', Empty , my_callback) # create the Service
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.spin() # mantain the service open.

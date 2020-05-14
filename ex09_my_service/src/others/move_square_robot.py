#! /usr/bin/env python
import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python class
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
from math import degrees, sqrt
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
pub = rospy.Publisher('/cmd_vel', Twist)


def move_forward():
    count.linear.x = 0.3
    count.angular.z = 0.0

def turn_left():
    count.linear.x = 0.0
    count.angular.z = 0.3

def stop():
    count.linear.x = 0.0
    count.angular.z = 0.0

def distance(x1,x2,y1,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def my_callback(request):
    global count
    global Flag, Flag1, Flag2
    print "moving robot"
    pub = rospy.Publisher('/cmd_vel', Twist)
    rate = rospy.Rate(2)
    count = Twist()
    i = 0
    c = 1
    #print angle
    init_position1 = x
    init_position2 = y
    init_angle = angle
    Flag = True
    sum = 0
    #move_forward()
    #print init_position1, init_position2, init_angle
    while not rospy.is_shutdown():
        print 1, x
        print degrees(angle)
        move_forward()
        if distance(0,x,0,0) >= 1:
            turn_left()
            if degrees(angle) > 85:
                stop()
                move_forward()
                if distance(0,x,y,0) >= sqrt(2):
                    stop()
                    turn_left()
                    if degrees(angle) > 175:
                        stop()
                        move_forward()
                        if distance(0,0,y,0) <= 0:
                            stop()

            sum = sum + 1
            print distance(0,x,0,0)



        pub.publish(count)
        rate.sleep()
    return EmptyResponse() # the service Response class, in this case EmptyResponse

#odom_sub = rospy.Subscriber('/odom', Odometry) #, position_robot)

rospy.init_node('service_move_square_robot')
my_service = rospy.Service('/my_service', Empty , my_callback) # create the Service
rospy.spin() # mantain the service open.

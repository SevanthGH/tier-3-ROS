#! /usr/bin/env python
import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python class
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
import math
from tf.transformations import euler_from_quaternion

x = y = z = angle = i = 0
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
    count.linear.x = 0.1
    count.angular.z = 0.0

def move_forward_in_y():
    count.linear.x = 0.3
    count.angular.z = 0.0

def turn_left():
    count.linear.x = 0.0
    count.angular.z = 0.1

def stop():
    count.linear.x = 0.0
    count.angular.z = 0.0

def distance(x1,x2,y1,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)



def my_callback(request):
    global count, i
    global Flag, Flag1, Flag2
    print "moving robot"
    pub = rospy.Publisher('/cmd_vel', Twist)
    rate = rospy.Rate(1)
    count = Twist()
    #i = 0
    #c = 1
    #print angle
    init_position1 = x
    init_position2 = y
    init_angle = angle
    Flag = True
    unit = 1
    #move_forward()
    if i >= 2:
        stop()
    #print init_position1, init_position2, init_angle
    #while not rospy.is_shutdown():
    while i < 2:
        move_forward()
        if x >= (unit + 0.1) and Flag == True:
            stop()
            turn_left()
            if angle >= 1.45 and Flag1 == True:
                stop()
                move_forward()
                if y >= (unit + 0.1):
                    turn_left()
                    if angle >= 3:
                        stop()
                        move_forward()
                        print 1
                        Flag = False
        if x <= -0.2 and Flag == False:
            stop()
            turn_left()
            print 2, x, y, math.degrees(angle)
            if (180 - abs(math.degrees(angle))) >= 85:
                stop()
                print 3
                move_forward()
                if y < -0.1:
                    print angle
                    stop()
                    turn_left()
                    if angle >= -0.1:
                        stop()
                        move_forward()
                        Flag = True
                        i = i + 1
        if i >= 2:
            stop()

        pub.publish(count)
        rate.sleep()
    return EmptyResponse() # the service Response class, in this case EmptyResponse

#odom_sub = rospy.Subscriber('/odom', Odometry) #, position_robot)

rospy.init_node('service_move_test_robot')
my_service = rospy.Service('/my_service', Empty , my_callback) # create the Service
rospy.spin() # mantain the service open.

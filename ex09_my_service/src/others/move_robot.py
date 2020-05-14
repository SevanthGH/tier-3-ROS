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
pub = rospy.Publisher('/cmd_vel', Twist)


def move_forward():
    count.linear.x = 0.3
    count.angular.z = 0.0

def move_forward_in_y():
    count.linear.x = 0.3
    count.angular.z = 0.0

def turn_left():
    count.linear.x = 0.0
    count.angular.z = 0.2

def stop():
    count.linear.x = 0.0
    count.angular.z = 0.0

def distance(x1,x2,y1,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def update_initial_position():
    #position_robot(msg)
    init_position1 = x
    init_position1 = y
    #print x, y

def other_half():
    if angle <= 3.1:
        turn_left()
    else:
        stop()


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
    #print init_position1, init_position2, init_angle
    while not rospy.is_shutdown():
        if (distance(x,init_position1,y,init_position2) <= 1):
            move_forward()
        #init_position1 = x
        #init_position2 = y
        if (distance(x,init_position1,y,init_position2) > 1):
            stop()
            if angle < 1.50 and Flag == True:
                print 1
                print angle
                turn_left()
            if angle >= 1.50:
                stop()
                #print x, y, angle
                if y <= 1:
                    move_forward_in_y()
                if y >= 1:
                    stop()
                    Flag = False
                    print x, y, angle
                    if angle <= 3.1 and Flag == False and Flag1 == True:
                        turn_left()
                        print 2, angle
                    if angle >= 3 or Flag1 == False:
                        if Flag2 == True:
                            stop()
                            Flag1 = False
                            print 3
                            if x > 0 and Flag2 == True:
                                move_forward()
                                print 4
                            if x < 0:
                                stop()
                                Flag2 = False
                                if angle <= 4.6:
                                    turn_left()
                                if angle >= 4.5:
                                    stop()

                    '''    if x >= 0:
                            move_forward_in_y()
                        if x < 0:
                            stop()
                    '''
            '''        if angle <= 3.1:
                        other_half()
                    if angle > 3.1:
                        stop()
                        if x >= -1:
                            move_forward()
                        else:
                            stop()
            '''
        '''                if x >= 1:
                            move_forward_in_y()
                        if x <= 0:
                            stop()
        '''
        '''        print x, y
                print distance(x,init_position1,y,init_position2)
                odom_sub = rospy.Subscriber('/odom', Odometry, position_robot)
                print x, y
                print init_position1, init_position2
                break
        '''        #update_initial_position()
        '''        if (distance(x,init_position1,y,init_position2) <= 1):
                    move_forward_in_y()
                if (distance(x,init_position1,y,init_position2) > 1):
                    stop()
        '''
        '''else:
            stop()
            if (angle < c*1.57):
                turn_left()
            else:
                if i < 3:
                    stop()
                    i = i+1
                    c = c+1'''
        pub.publish(count)
        rate.sleep()
    return EmptyResponse() # the service Response class, in this case EmptyResponse

#odom_sub = rospy.Subscriber('/odom', Odometry) #, position_robot)

rospy.init_node('service_move_robot')
my_service = rospy.Service('/my_service', Empty , my_callback) # create the Service
rospy.spin() # mantain the service open.

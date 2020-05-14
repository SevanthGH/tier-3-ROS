#! /usr/bin/env python
import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python class

def my_callback(request):
    print "My callback has been called"
    return EmptyResponse() # the service Response class, in this case EmptyResponse

rospy.init_node('service_client')
my_service = rospy.Service('/my_service', Empty , my_callback) # create the Service
rospy.spin() # mantain the service open.


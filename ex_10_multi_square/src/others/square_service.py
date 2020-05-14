#! /usr/bin/env python
import rospy
from ex10_my_srv_msg.srv import MyServiceMsg, MyServiceMsgResponse

def my_callback(request):
    my_response = MyServiceMsgResponse()
    if request.radius > 5.0:
        my_response.success = True
    else:
        my_response.success = False
    return my_response # the service Response class, in this case MyCustomServiceMessage

rospy.init_node('service_client')
my_service = rospy.Service('/my_service', MyServiceMsg, my_callback)
rospy.spin()


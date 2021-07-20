#!/usr/bin/env python3

import numpy as np
import rospy

from std_msgs.msg import Float64MultiArray, MultiArrayDimension

pub = rospy.Publisher('chatter', Float64MultiArray, queue_size=10)
rospy.init_node('master')  
rate = rospy.Rate(10) # 10hz

def talker():
    while not rospy.is_shutdown():
        message = Float64MultiArray()
        message.layout.data_offset = 0
        dim = []
        dim.append(MultiArrayDimension("length", 1, 1))
        dim.append(MultiArrayDimension("Width", 1 , 1))
        message.layout.dim = dim
        rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python3

import numpy as np
import rospy as rp

from std_msgs.msg import String

rp.init_node('master')

pub = rp.Publisher('chatter', String, queue_size=10)
rate = rp.Rate(10) # 10hz

def talker():
    while not rp.is_shutdown():
        hello_str = "hello world %s" % rp.get_time()
        rp.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rp.ROSInterruptException:
        pass
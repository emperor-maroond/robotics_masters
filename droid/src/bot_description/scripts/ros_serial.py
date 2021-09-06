#!/usr/bin/env python3

import numpy as np
import rospy

from my_message.msg import my_message

def callback(data):
    servoFeed_R = data.some_floats[0]
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2]
    encoder_2 = data.some_floats[3]

    print(servoFeed_R)
    print(servoFeed_L)
    print(encoder_1)
    print(encoder_2)

def listener():
    try:
        rospy.init_node('data_slave', disable_signals=True)
        rospy.Subscriber("sensor_data", my_message, callback)
        # rospy.spin()
        while not rospy.core.is_shutdown():
            rospy.rostime.wallsleep(0.5)
    except KeyboardInterrupt:
        print('Adios!')

if __name__ == '__main__':
    listener()
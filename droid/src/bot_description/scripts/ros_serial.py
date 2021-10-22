#!/usr/bin/env python3

import numpy as np
import rospy

from my_message.msg import my_message

# Some arrays to store the data that will be dumped in a text file
tmp1 = []
tmp2 = []
tmp3 = []
tmp4 = []

def callback(data):
    servoFeed_R = data.some_floats[0]
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2]
    encoder_2 = data.some_floats[3]

    print(servoFeed_R, servoFeed_L, encoder_1, encoder_2)

    tmp1.append(servoFeed_R)
    tmp2.append(servoFeed_L)
    tmp3.append(encoder_1)
    tmp4.append(encoder_2)

def listener():
    try:
        rospy.init_node('data_slave', disable_signals=True)
        rospy.Subscriber("sensor_data", my_message, callback)
        # rospy.spin()
        while not rospy.core.is_shutdown():
            rospy.rostime.wallsleep(0.5)
    except KeyboardInterrupt:
        file = open('data.txt', 'w')
        file.write('Servo Feedback Right:\n {}\n'.format(tmp1))
        file.write('Servo Feedback Left:\n {}\n'.format(tmp2))
        file.write('Encoder data 1:\n {}\n'.format(tmp3))
        file.write('Encoder data 2:\n {}\n'.format(tmp4))
        file.close()
        print('Adios!')

if __name__ == '__main__':
    listener()
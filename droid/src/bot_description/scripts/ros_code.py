#!/usr/bin/env python3

import numpy as np
import rospy as rp
import cloudpickle
import time

from my_message.msg import my_message

pub = rp.Publisher('chatter', my_message, queue_size=10)
rp.init_node('master')  
message = my_message()
message.some_floats = []

data = [0]*3

with open("accel.pkl", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("steady-state.pkl", "rb") as f:
    data[1] = cloudpickle.load(f)      

with open("decel.pkl", "rb") as f:
    data[2] = cloudpickle.load(f)

def accel():
    global message
    N = data[0].N[-1]
    for n in range(1, N+1):
        message.some_floats.append(data[0].q0[n, 'theta_l_R'].value - np.pi/2)
        message.some_floats.append(data[0].q0[n, 'theta_l_L'].value - np.pi/2)
        message.some_floats.append(data[0].Fbang_pos_R[n].value - data[0].Fbang_neg_R[n].value)
        message.some_floats.append(data[0].Fbang_pos_L[n].value - data[0].Fbang_neg_L[n].value)

        # rp.loginfo(message)
        rp.loginfo('accel')
        pub.publish(message)
        message.some_floats.clear()

        sleep = data[0].h[n].value
        rp.sleep(sleep)

def steady_state():
    global message
    N = data[1].N[-1]
    for n in range(1, N+1):
        message.some_floats.append(data[1].q0[n, 'theta_l_R'].value - np.pi/2)
        message.some_floats.append(data[1].q0[n, 'theta_l_L'].value - np.pi/2)
        message.some_floats.append(data[1].Fbang_pos_R[n].value - data[1].Fbang_neg_R[n].value)
        message.some_floats.append(data[1].Fbang_pos_L[n].value - data[1].Fbang_neg_L[n].value)

        # rp.loginfo(message)
        rp.loginfo('steady-state')
        pub.publish(message)
        message.some_floats.clear()

        sleep = data[1].h[n].value
        rp.sleep(sleep)

def decel():
    global message
    N = data[2].N[-1]
    for n in range(1, N+1):
        message.some_floats.append(data[2].q0[n, 'theta_l_R'].value - np.pi/2)
        message.some_floats.append(data[2].q0[n, 'theta_l_L'].value - np.pi/2)
        message.some_floats.append(data[2].Fbang_pos_R[n].value - data[2].Fbang_neg_R[n].value)
        message.some_floats.append(data[2].Fbang_pos_L[n].value - data[2].Fbang_neg_L[n].value)

        # rp.loginfo(message)
        rp.loginfo('decel')
        pub.publish(message)
        message.some_floats.clear()

        sleep = data[2].h[n].value
        rp.sleep(sleep)

if __name__ == '__main__':
    try:
        accel()
        steady_state()
        decel()
    except rp.ROSInterruptException:
        pass
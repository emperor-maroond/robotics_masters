#!/usr/bin/env python3

import numpy as np
import rospy as rp
import cloudpickle
import time

from std_msgs.msg import Float64
from std_srvs.srv import Empty

rp.init_node('commander')

reset_simulation = rp.ServiceProxy('/gazebo/reset_simulation', Empty)

pub = [None]*4

pub[0] = rp.Publisher("/bot/RevR_position_controller/command", Float64, queue_size=10)
pub[1] = rp.Publisher("/bot/RevL_position_controller/command", Float64, queue_size=10)
pub[2] = rp.Publisher("/bot/SliderR_position_controller/command", Float64, queue_size=10)
pub[3] = rp.Publisher("/bot/SliderL_position_controller/command", Float64, queue_size=10)

data = [None]*3

with open("accel.pkl", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("steady-state.pkl", "rb") as f:
    data[1] = cloudpickle.load(f)      

with open("decel.pkl", "rb") as f:
    data[2] = cloudpickle.load(f)


def accel():
    N = data[0].N[-1]
    for n in range(1, N+1):
        pub[0].publish(data[0].q0[n, 'theta_l_R'].value - np.pi/2)
        pub[1].publish(data[0].q0[n, 'theta_l_L'].value - np.pi/2)
        F = data[0].F_max*(data[0].Fbang_pos_R[n].value - data[0].Fbang_neg_R[n].value)
        pub[2].publish(F)
        F = data[0].F_max*(data[0].Fbang_pos_L[n].value - data[0].Fbang_neg_L[n].value)
        pub[3].publish(F)

        sleep = data[0].h[n].value
        rp.sleep(sleep)

def steady_state():
    N = data[1].N[-1]
    for n in range(1, N+1):
        pub[0].publish(data[1].q0[n, 'theta_l_R'].value - np.pi/2)
        pub[1].publish(data[1].q0[n, 'theta_l_L'].value - np.pi/2)
        F = data[1].F_max*(data[1].Fbang_pos_R[n].value - data[1].Fbang_neg_R[n].value)
        pub[2].publish(F)
        F = data[1].F_max*(data[1].Fbang_pos_L[n].value - data[1].Fbang_neg_L[n].value)
        pub[3].publish(F)

        sleep = data[1].h[n].value
        rp.sleep(sleep)

def decel():
    N = data[2].N[-1]
    for n in range(1, N+1):
        pub[0].publish(data[2].q0[n, 'theta_l_R'].value - np.pi/2)
        pub[1].publish(data[2].q0[n, 'theta_l_L'].value - np.pi/2)
        F = data[2].F_max*(data[2].Fbang_pos_R[n].value - data[2].Fbang_neg_R[n].value)
        pub[2].publish(F)
        F = data[2].F_max*(data[2].Fbang_pos_L[n].value - data[2].Fbang_neg_L[n].value)
        pub[3].publish(F)

        sleep = data[2].h[n].value
        rp.sleep(sleep)

if __name__ == '__main__': 
    reset_simulation()

    pub[0].publish(data[0].q0[1, 'theta_l_R'].value - np.pi/2)
    pub[1].publish(data[0].q0[1, 'theta_l_L'].value - np.pi/2)
    pub[2].publish(-data[0].F_max)
    pub[3].publish(-data[0].F_max)

    time.sleep(2)

    accel()
    steady_state()
    steady_state()
    steady_state()
    decel()
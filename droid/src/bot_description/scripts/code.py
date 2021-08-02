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

with open("Feasible_Solution/1/accel.pkl", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("Feasible_Solution/1/steady-state.pkl", "rb") as f:
    data[1] = cloudpickle.load(f)      

with open("Feasible_Solution/1/decel.pkl", "rb") as f:
    data[2] = cloudpickle.load(f)

run_time = []
adder = 0
N = data[0].N[-1]
cN = data[0].cN[-1]
for i in range(0, 3):
    if(i>0):
        adder += (data[i-1].tt[N,cN].value - data[i-1].tt[1,1].value)
    for n in range(1, N+1):
        for c in range(1, cN+1):
            run_time.append(data[i].tt[n,c].value - data[i].tt[1,1].value + adder)

def accel():
    N = data[0].N[-1]
    cN = data[0].cN[-1]
    i = 0
    for n in range(1, N+1):
        for c in range(1, cN+1):
            pub[0].publish(data[0].q[n,c, 'theta_l_R'].value )
            pub[1].publish(data[0].q[n,c, 'theta_l_L'].value )
            if c == cN:
                F = data[0].F_max*(np.round(data[0].Fbang_pos_R[n].value) - np.round(data[0].Fbang_neg_R[n].value))
                pub[2].publish(F)
                F = data[0].F_max*(np.round(data[0].Fbang_pos_L[n].value) - np.round(data[0].Fbang_neg_L[n].value))
                pub[3].publish(F)

            # sleep = data[0].h[n].value
            sleep = run_time[i+1] - run_time[i]
            rp.sleep(sleep)
            i += 1

def steady_state():
    N = data[1].N[-1]
    cN = data[1].cN[-1]
    i = 0
    for n in range(1, N+1):
        for c in range(1, cN+1):
            pub[0].publish(data[1].q[n,c, 'theta_l_R'].value )
            pub[1].publish(data[1].q[n,c, 'theta_l_L'].value )
            if c == cN:
                F = data[1].F_max*(np.round(data[1].Fbang_pos_R[n].value) - np.round(data[1].Fbang_neg_R[n].value))
                pub[2].publish(F)
                F = data[1].F_max*(np.round(data[1].Fbang_pos_L[n].value) - np.round(data[1].Fbang_neg_L[n].value))
                pub[3].publish(F)

            # sleep = data[1].h[n].value
            sleep = run_time[N+i+1] - run_time[N+i]
            rp.sleep(sleep)
            i += 1

def decel():
    N = data[2].N[-1]
    cN = data[2].cN[-1]
    i = 0
    for n in range(1, N+1):
        for c in range(1, cN+1):
            pub[0].publish(data[2].q[n,c, 'theta_l_R'].value )
            pub[1].publish(data[2].q[n,c, 'theta_l_L'].value )
            if c == cN:
                F = data[2].F_max*(np.round(data[2].Fbang_pos_R[n].value) - np.round(data[2].Fbang_neg_R[n].value))
                pub[2].publish(F)
                F = data[2].F_max*(np.round(data[2].Fbang_pos_L[n].value) - np.round(data[2].Fbang_neg_L[n].value))
                pub[3].publish(F)

            # sleep = data[2].h[n].value
            sleep = run_time[2*N+i+1] - run_time[2*N+i]
            rp.sleep(sleep)
            i += 1

if __name__ == '__main__': 
    reset_simulation()

    pub[0].publish(data[0].q0[1, 'theta_l_R'].value )
    pub[1].publish(data[0].q0[1, 'theta_l_L'].value )
    pub[2].publish(-data[0].F_max)
    pub[3].publish(-data[0].F_max)

    time.sleep(2)

    accel()
    steady_state()
    decel()
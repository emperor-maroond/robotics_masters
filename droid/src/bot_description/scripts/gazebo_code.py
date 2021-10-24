#!/usr/bin/env python3

import numpy as np
import rospy as rp
import cloudpickle
import time

from std_msgs.msg import Float64
from std_srvs.srv import Empty

# Set-up ROS and read in trajectory data_________________________________________________________

rp.init_node('commander')

pub_time = 20/1000
rate = rp.Rate(1/pub_time)

reset_simulation = rp.ServiceProxy('/gazebo/reset_simulation', Empty)

pub = [None]*4

pub[0] = rp.Publisher("/bot/RevR_position_controller/command", Float64, queue_size=10)
pub[1] = rp.Publisher("/bot/RevL_position_controller/command", Float64, queue_size=10)
pub[2] = rp.Publisher("/bot/SliderR_position_controller/command", Float64, queue_size=10)
pub[3] = rp.Publisher("/bot/SliderL_position_controller/command", Float64, queue_size=10)

data = [None]*3

with open("Feasible_Solution/short1/accel.pkl", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("Feasible_Solution/short1/steady-state.pkl", "rb") as f:
    data[1] = cloudpickle.load(f)

with open("Feasible_Solution/short1/decel.pkl", "rb") as f:
    data[2] = cloudpickle.load(f)

# Code__________________________________________________________________________________________

# Var for data that will be interpolated
F_max = data[0].F_max
theta_L  = []
theta_R  = []
F_bang_L = []
F_bang_R = []
position_N = 0
position_cN = 0

# Var for data that will be published
servo_R = []
servo_L = []
solenoid_R = []
solenoid_L = []

# Var that will hold run time
run_time = 0
N_time = []
cN_time = []
N_adder = 0
cN_adder = 0

def accel():
    N = data[0].N[-1]
    cN = data[0].cN[-1]
    for n in range(1, N+1):
        F_bang_R.append(data[0].Fbang_pos_R[n].value - data[0].Fbang_neg_R[n].value)
        F_bang_L.append(data[0].Fbang_pos_L[n].value - data[0].Fbang_neg_L[n].value)
        N_time.append(data[0].tt0[n].value - data[0].tt0[1].value)
        for c in range(1, cN+1):
            theta_R.append(data[0].q[n,c,'theta_l_R'].value)
            theta_L.append(data[0].q[n,c,'theta_l_L'].value)
            cN_time.append(data[0].tt[n,c].value - data[0].tt[1,1].value)

def steady_state():
    global N_adder, cN_adder
    N = data[1].N[-1]
    cN = data[1].cN[-1]
    N_adder += (data[0].tt0[N].value - data[0].tt0[1].value)
    cN_adder += (data[0].tt[N,cN].value - data[0].tt[1,1].value)
    for n in range(1, N+1):
        F_bang_R.append(data[1].Fbang_pos_R[n].value - data[1].Fbang_neg_R[n].value)
        F_bang_L.append(data[1].Fbang_pos_L[n].value - data[1].Fbang_neg_L[n].value)
        N_time.append(data[1].tt0[n].value - data[1].tt0[1].value + N_adder)
        for c in range(1, cN+1):
            theta_R.append(data[1].q[n,c,'theta_l_R'].value)
            theta_L.append(data[1].q[n,c,'theta_l_L'].value)
            cN_time.append(data[1].tt[n,c].value - data[1].tt[1,1].value + cN_adder)

def decel():
    global N_adder, cN_adder
    N = data[2].N[-1]
    cN = data[2].cN[-1]
    N_adder += (data[1].tt0[N].value - data[1].tt0[1].value)
    cN_adder += (data[1].tt[N,cN].value - data[1].tt[1,1].value)
    for n in range(1, N+1):
        F_bang_R.append(data[2].Fbang_pos_R[n].value - data[2].Fbang_neg_R[n].value)
        F_bang_L.append(data[2].Fbang_pos_L[n].value - data[2].Fbang_neg_L[n].value)
        N_time.append(data[2].tt0[n].value - data[2].tt0[1].value + N_adder)
        for c in range(1, cN+1):
            theta_R.append(data[2].q[n,c,'theta_l_R'].value)
            theta_L.append(data[2].q[n,c,'theta_l_L'].value)
            cN_time.append(data[2].tt[n,c].value - data[2].tt[1,1].value + cN_adder)

def interpolate(y, cur_time, x, position):
    # y = data
    # x = time
    ans = 0
    for i in range(position, len(x)):
        if(x[i]<=cur_time and cur_time<x[i+1]):
            position = i
            ans = y[i] + (cur_time - x[i])*(y[i+1] - y[i])/(x[i+1] - x[i])
            return ans, position

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

    while 1:
        if(run_time>N_time[-1]):
            break

        tmp, position_cN = interpolate(theta_R, run_time, cN_time, position_cN)
        servo_R.append(tmp)
        tmp, position_cN = interpolate(theta_L, run_time, cN_time, position_cN)
        servo_L.append(tmp)

        tmp, position_N = interpolate(F_bang_R, run_time, N_time, position_N)
        solenoid_R.append(F_max * np.round(tmp))
        tmp, position_N = interpolate(F_bang_L, run_time, N_time, position_N)
        solenoid_L.append(F_max * np.round(tmp))

        run_time += pub_time

    i = 0
    while not rp.is_shutdown():
        if(i>=len(servo_R)):
            break

        pub[0].publish(servo_R[i]) # theta_l_R
        pub[1].publish(servo_L[i]) # theta_l_L)
        pub[2].publish(solenoid_R[i]) # F_bang_R
        pub[3].publish(solenoid_L[i]) # F_bang_L
        i += 1
        rate.sleep()

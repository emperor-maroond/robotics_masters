#!/usr/bin/env python3

import numpy as np
import rospy
import cloudpickle

from my_message.msg import my_message

# Set-up ROS and read in trajectory data_________________________________________________________

rospy.init_node('master')

pub_time = 10/1000
# rate = rospy.Rate(1/pub_time)
rate = rospy.Rate(1000)

pub = rospy.Publisher('chatter', my_message, queue_size=10)
  
message = my_message()
message.some_floats = []

data = [None]*3

with open("Feasible_Solution/00/accel.pkl", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("Feasible_Solution/00/steady-state.pkl", "rb") as f:
    data[1] = cloudpickle.load(f)      

with open("Feasible_Solution/00/decel.pkl", "rb") as f:
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

def end():
    servo_R.append(-10)
    servo_L.append(-10)
    solenoid_R.append(-10)
    solenoid_L.append(-10)

def interpolate(y, cur_time, x, position):
    # y = data
    # x = time
    ans = 0
    for i in range(position, len(x)):
        if(x[i]<=cur_time and cur_time<x[i+1]):
            position = i
            ans = y[i] + (cur_time - x[i])*(y[i+1] - y[i])/(x[i+1] - x[i])
            return ans, position

def send_message():
    global message
    rospy.loginfo('send data')
    for n in range(0, len(servo_R)):
        message.some_floats.append(servo_R[n])
        message.some_floats.append(servo_L[n])
        message.some_floats.append(solenoid_R[n])
        message.some_floats.append(solenoid_L[n])

        rospy.loginfo(message)
        pub.publish(message)
        message.some_floats.clear()

        rate.sleep()

if __name__ == '__main__':
    accel()
    steady_state()
    decel()

    while 1:
        if(run_time>N_time[-1]):
            end()
            break

        tmp, position_cN = interpolate(theta_R, run_time, cN_time, position_cN)
        servo_R.append(tmp)
        tmp, position_cN = interpolate(theta_L, run_time, cN_time, position_cN)
        servo_L.append(tmp)

        tmp, position_N = interpolate(F_bang_R, run_time, N_time, position_N)
        solenoid_R.append(np.round(tmp))
        tmp, position_N = interpolate(F_bang_L, run_time, N_time, position_N)
        solenoid_L.append(np.round(tmp))

        run_time += pub_time

    try:
        send_message()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python3

import numpy as np
import rospy as rp
import cloudpickle

from my_message.msg import my_message

# Set-up ROS and read in trajectory data_________________________________________________________

rp.init_node('master')

pub_time = 10/1000
# rate = rp.Rate(1/pub_time)
rate = rp.Rate(1/pub_time)

pub = rp.Publisher('chatter', my_message, queue_size=10)
  
message = my_message()
message.some_floats = []

data = [None]*3

with open("Feasible_Solution/short1/accel.pkl", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("Feasible_Solution/short1/steady-state.pkl", "rb") as f:
    data[1] = cloudpickle.load(f)      

with open("Feasible_Solution/short1/decel.pkl", "rb") as f:
    data[2] = cloudpickle.load(f)


# Code__________________________________________________________________________________________
def d2r(deg):
    return deg*np.pi/180

def r2d(rad):
    return rad*180/np.pi


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

# For holding message data
dat = [None]*4
dat[0] = 0 # Rev Right
dat[1] = 0 # Rev Left
dat[2] = 0 # Slider Right
dat[3] = 0 # Slider Left

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
    # rp.loginfo('send data:')
    for n in range(0, len(dat)):
        message.some_floats.append(dat[n])
    
    # rp.loginfo(message)
    pub.publish(message)
    message.some_floats.clear()


# Callback______________________________________________________________________________
ser_R = []
ser_L = []
enc_1 = []
enc_2 = []

i = 0

def callback(data):
    global ser_R, ser_L, enc_1, enc_2
    servoFeed_R = data.some_floats[0] 
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2] # Height
    encoder_2 = data.some_floats[3] # Length travled
    rad = d2r(encoder_1)

    ser_R.append(servoFeed_R)
    ser_L.append(servoFeed_L)
    enc_1.append(encoder_1)
    enc_2.append(encoder_2)

    if round(servoFeed_R,5) == round(servo_R[i],5) and round(servoFeed_L,5) == round(servo_L[i],5):
        i+=1
        dat[0] = servo_R[i]
        dat[1] = servo_L[i]
        dat[2] = solenoid_R[i]
        dat[3] = solenoid_L[i]
        
        if i >= len(servo_R):
            i = len(servo_R) - 1
        
    send_message()

def listener():
    try:
        rp.Subscriber('sensor_data', my_message, callback)
        while not rp.core.is_shutdown():
            rp.rostime.wallsleep(0.5)
    except KeyboardInterrupt:
        # destroy()
        # rp.signal_shutdown("Adios")
        print('Bye')
        
        file = open('/home/devlon/robotics_masters/data.txt', 'a')
        file.write('Servo Feedback Right:\n {}\n'.format(ser_R))
        file.write('Servo Feedback Left:\n {}\n'.format(ser_L))
        file.write('Encoder data 1:\n {}\n'.format(enc_1))
        file.write('Encoder data 2:\n {}\n'.format(enc_2))
        file.close()
        # print('Adios!')

if __name__ == '__main__':
    accel()
    steady_state()
    decel()

    while 1:
        if(run_time>N_time[-1]):
            end()
            break

        tmp, position_cN = interpolate(theta_R, run_time, cN_time, position_cN)
        servo_R.append(r2d(tmp))
        tmp, position_cN = interpolate(theta_L, run_time, cN_time, position_cN)
        servo_L.append(r2d(tmp)) 

        tmp, position_N = interpolate(F_bang_R, run_time, N_time, position_N)
        if tmp >= 0.13:
            solenoid_R.append(np.ceil(tmp))
        elif tmp <= -0.13:
            solenoid_R.append(np.floor(tmp))   
        else:
            solenoid_R.append(np.round(tmp))
        tmp, position_N = interpolate(F_bang_L, run_time, N_time, position_N)
        if tmp >= 0.13:
            solenoid_L.append(np.ceil(tmp))
        elif tmp <= -0.13:
            solenoid_L.append(np.floor(tmp))   
        else:
            solenoid_L.append(np.round(tmp))

        run_time += pub_time

    try:
        dat[0] = servo_R[i]
        dat[1] = servo_L[i]
        dat[2] = solenoid_R[i]
        dat[3] = solenoid_L[i]
        listener()
    except rp.ROSInterruptException:
        pass
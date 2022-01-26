#!/usr/bin/env python3

from concurrent.futures import process, thread
from curses import tigetflag
from signal import SIGINT, siginterrupt, signal
import numpy as np
import rospy as rp
import time
import pyautogui

from math import isclose
from std_msgs.msg import Float64
from std_srvs.srv import Empty
from my_message.msg import my_message

rp.init_node('master')

pub_time = 10/1000
rate = rp.Rate(1/pub_time)

pub = rp.Publisher('chatter', my_message, queue_size=10)

message = my_message()
message.some_floats = []

# Functions__________________________________________________________________________________
firing = False
boom = 0

dat = [None]*5

dat[0] = 0 # Rev Right
dat[1] = 0 # Rev Left
dat[2] = 0 # Slider Right
dat[3] = 0 # Slider Left
dat[4] = 0 # Offset

def d2r(deg):
    return deg*np.pi/180

def r2d(rad):
    return rad*180/np.pi

def move(start, stop, z):
    delta = stop - start
    if abs(delta)>d2r(17):
        q = delta/300*z
    else:
        q = delta/200*z
    return start + q

def test_boom():
    global firing, boom
    delay = time.time()*1000 - boom
    if delay<160:
        firing = True
    else:
        firing = False

def send_message():
    global message
    # rp.loginfo('send data:')
    for n in range(0, len(dat)):
        message.some_floats.append(dat[n])
    
    # rp.loginfo(message)
    pub.publish(message)
    message.some_floats.clear()
    
# States_____________________________________________________________________________________
flag = 1
done = 0
start_R = 0
end_R   = 0
start_L = 0
end_L   = 0
z = 1
triggered = 1

i = 0
ground = False
apex = False
run = True
avg = -0.22
devider = 0
ref_height = 0
arm_len = 1
startup = True
offset = 0

ser_R = []
ser_L = []
enc_1 = []
enc_2 = []

def state_0():  # START state as well as STOP state
    global end_R, end_L, done
    end_R = d2r(90)
    end_L = d2r(90)
    dat[0] = end_R
    dat[1] = end_L
    dat[2] = -1
    dat[3] = -1
    dat[4] = offset
    done = 1

def state_1():
    global flag, start_R, end_R, start_L, end_L, z, done, boom
    if flag:
        done = 0
        global R, L
        R = end_R
        L = end_L
        flag = 0
        start_R = end_R
        start_L = end_L
        end_R = d2r(90)
        end_L = d2r(90)
        dat[2] = -1
        dat[3] = -1
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        if R==end_R and L==end_L:
            dat[2] = 1
            dat[3] = 1
            if not done:
                boom = time.time()*1000
            z = 0
            done = 1
    dat[0] = R
    dat[1] = L
    dat[4] = offset

def state_2():
    global flag, start_R, end_R, start_L, end_L, z, done, boom
    if flag:
        global R, L
        done = 0
        R = end_R
        L = end_L        
        flag = 0
        start_R = end_R
        start_L = end_L
        end_R = d2r(90)
        end_L = d2r(90)
        dat[2] = 1
        dat[3] = 1        
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        if R==end_R and L==end_L:
            z = 0
            dat[2] = -1
            dat[3] = -1
            if not done:
                boom = time.time()*1000
            done = 1
    dat[0] = R
    dat[1] = L
    dat[4] = offset

# Callback code_________________________________________________________________________
states = [state_0, state_1, state_2]

def callback(data):
    global i, apex, flag, ground, run, done, ref_height, startup, offset, triggered
    global ser_R, ser_L, enc_1, enc_2
    servoFeed_R = data.some_floats[0]
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2] # assume this is height
    encoder_2 = data.some_floats[3]
    rad = d2r(encoder_1)
    test_boom()
    
    if startup:
        startup = False
        ref_height = np.sin(rad)*arm_len
        delay = time.time()*1000

        while time.time()*1000-delay <= 3000:
            states[0]()
            send_message()

    offset = rad

    height = np.sin(rad)*arm_len - ref_height
    
    # print(r2d(offset), height)

    if run:
        states[i]()
    
    dat[4] = offset
    send_message()

    if not firing:
        if done:
            if not ground and i>0:
                print(i, 'a')
                ground = True
            elif ground and not apex:
                print(i, "b")
                apex = True
            elif apex and ground:
                print(i, 'c')
                ground = apex = False
            done = 0
            run = False
            i += 1
            flag = 1
            triggered = 0
        
        if height<=50/1000:                       # Check the correct height
            if not ground:
                run = True
                flag = 1
                triggered = 1
        if height>200/1000.0 and not apex:
            if not apex and ground and i>0:
                run = True
                flag = 1
                triggered = 1
        if height>200/1000.0 and apex:
            if ground and apex and i>0:
                run = True
                flag = 1
                triggered = 1
    
    ser_R.append(servoFeed_R)
    ser_L.append(servoFeed_L)
    enc_1.append(encoder_1)
    enc_2.append(encoder_2)

    if i >= len(states):
        i = len(states)-1
        # pyautogui.hotkey('ctrl', 'c')

def listener():
    try:
        rp.Subscriber('sensor_data', my_message, callback)
        while not rp.core.is_shutdown():
            rp.rostime.wallsleep(0.5)
    except KeyboardInterrupt:
        # destroy()
        # rp.signal_shutdown("Adios")
        print('Bye')
        
        file = open('data.txt', 'a')
        file.write('Servo Feedback Right:\n {}\n'.format(ser_R))
        file.write('Servo Feedback Left:\n {}\n'.format(ser_L))
        file.write('Encoder data 1:\n {}\n'.format(enc_1))
        file.write('Encoder data 2:\n {}\n'.format(enc_2))
        file.close()
        print('Adios!')


# main code_____________________________________________________________________
if __name__ == '__main__':
    listener()
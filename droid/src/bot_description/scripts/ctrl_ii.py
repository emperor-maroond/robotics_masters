#!/usr/bin/env python3

import numpy as np
from sympy import ground_roots
import rospy as rp
import time
import pyautogui

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

dat = [None]*4

dat[0] = 0 # Rev Right
dat[1] = 0 # Rev Left
dat[2] = 0 # Slider Right
dat[3] = 0 # Slider Left

def d2r(deg):
    return deg*np.pi/180

def r2d(rad):
    return rad*180/np.pi

def move(end, current):
    smootedMotion = (0.3*end) + (0.7*current)
    return smootedMotion


def test_boom():
    global firing, boom
    delay = time.time()*1000 - boom
    if delay<200:
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
i = 0
j = 0
arm_len = 1
startup = 1
ref_height = 0
height = None
done = True

ser_R = []
ser_L = []
enc_1 = []
enc_2 = []

class acel():
    def rest():
        end_R = d2r(120)
        end_L = d2r(60)
        dat[0] = end_R
        dat[1] = end_L
        dat[2] = -1
        dat[3] = -1

    def ground():
        global done
        end_R = d2r(115.53)
        end_L = d2r(70.54)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        dat[2] = -1
        dat[3] = -1
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = 1
            dat[3] = 1
            done = True

    def air():
        global done
        end_R = d2r(125.80)
        end_L = d2r(89.80 )
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        dat[2] = 1
        dat[3] = 1
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = 1
            dat[3] = 1
            done = True

class steady_state():
    def ground():
        global done
        end_R = d2r(67.86)
        end_L = d2r(129.14)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        dat[2] = 1
        dat[3] = 1
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            steady_state.ground2()

    def ground2():
        global done
        end_R = d2r(100.10)
        end_L = d2r(136.65)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        dat[2] = -1
        dat[3] = -1
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = 1
            dat[3] = 1
            done = True

    def air():
        global done
        end_R = d2r(125.80)
        end_L = d2r(89.80 )
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        dat[2] = 1
        dat[3] = 1
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = 1
            dat[3] = 1
            done = True

class decel():
    def ground():
        global done
        end_R = d2r(120)
        end_L = d2r(60)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        dat[2] = 1
        dat[3] = 1
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            done = True

    def air():
        pass

# Callback code_________________________________________________________________________
ground = [acel.ground, steady_state.ground, decel.ground]
air = [acel.air, steady_state.air]

states = [ground, air]

def callback(data):
    global i, j, ref_height, startup, done, boom
    global ser_R, ser_L, enc_1, enc_2
    servoFeed_R = data.some_floats[0] 
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2] # Height
    encoder_2 = data.some_floats[3] # Length travled
    rad = d2r(encoder_1)
    
    test_boom()
    
    if startup:
        startup = False
        ref_height = np.sin(rad)*arm_len
        delay = time.time()*1000

        while time.time()*1000-delay <= 3000:
            acel.rest()
            send_message()

    height = np.sin(rad)*arm_len - ref_height
    
    if j == 0:
        states[j][i/2]
    elif j == 1:
        states[j][(i-1)/2]
    send_message()

    # print(i)
    if not firing:
        # print(height*1000, i)
        if height<300/1000: # Check the correct height
            if done and j == 0:
                i += 1
                j += 1
                done = False
        elif height>=300/1000:
            if done and j == 1:
                i += 1
                j -= 1
                done = False
    
    if i >= len(states)[1]:
        i = len(states)[1] - 1
        # pyautogui.hotkey('ctrl', 'c')

    ser_R.append(servoFeed_R)
    ser_L.append(servoFeed_L)
    enc_1.append(encoder_1)
    enc_2.append(encoder_2)

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


# main code_____________________________________________________________________
if __name__ == '__main__':
    listener()
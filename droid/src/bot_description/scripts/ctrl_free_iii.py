#!/usr/bin/env python3

import numpy as np
import rospy as rp
import time
import signal
import sys

from my_message.msg import my_message

rp.init_node('master')

pub_time = 5/1000
rate = rp.Rate(1/pub_time)

pub = rp.Publisher('chatter', my_message, queue_size=1)

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

def sigint_handler(signal, frame):
    file = open('data.csv', 'w')
    file.write('Servo Feedback Right:\n {}\n'.format(ser_R))
    file.write('Servo Feedback Left:\n {}\n'.format(ser_L))
    file.write('Encoder data 1:\n {}\n'.format(enc_1))
    file.write('Encoder data 2:\n {}\n'.format(enc_2))
    file.write('Encoder data 3:\n {}\n'.format(enc_3))
    file.close()

    acel.rest()
    send_message()
    print ('KeyboardInterrupt is caught')
    sys.exit(0)

def d2r(deg):
    return deg*np.pi/180

def r2d(rad):
    return rad*180/np.pi

def move(end, current):
    ratio = 0.001
    smootedMotion = ((1-ratio)*end) + (ratio*current)
    return smootedMotion

def test_boom():
    global firing, boom
    delay = time.time()*1000 - boom
    if delay<20:
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
arm_len = 0.84
startup = 1
ref_height = 0
height = None
done = True

ser_R = []
ser_L = []
enc_1 = []
enc_2 = []
enc_3 = []

class acel():
    def rest():
        end_R = d2r(65)
        end_L = d2r(110)
        dat[0] = end_R
        dat[1] = end_L
        dat[2] = -1
        dat[3] = -1

    def ground():
        global done, boom
        end_R = d2r(65)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = 1
            #boom = time.time()*1000
            done = True

    def air():
        global done, boom
        dat[2] = -1
        dat[3] = -1
        end_R = d2r(110)
        end_L = d2r(65)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            boom = time.time()*1000
            done = True

class steady_state():
    def ground():
        global done, i, boom
        end_R = d2r(110)
        end_L = d2r(65)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            i += 1
            boom = time.time()*1000

    def ground2():
        global done
        end_R = d2r(110)
        end_L = d2r(65)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = 1
            dat[3] = -1
            done = True

    def air1():
        global done, boom
        dat[2] = -1
        dat[3] = -1
        end_R = d2r(65)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            boom = time.time()*1000
            done = True

    def ground3():
        global done, i, boom
        end_R = d2r(65)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            i += 1
            boom = time.time()*1000

    def ground4():
        global done
        end_R = d2r(65)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = 1
            done = True

    def air2():
        global done, boom
        dat[2] = -1
        dat[3] = -1
        end_R = d2r(110)
        end_L = d2r(65)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            boom = time.time()*1000
            done = True

class decel():
    def ground():
        global done
        end_R = d2r(110)
        end_L = d2r(65)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -1
            dat[3] = -1
            done = True
        

# Callback code_________________________________________________________________________
ground = [acel.ground, steady_state.ground, steady_state.ground2, steady_state.ground3, steady_state.ground4, steady_state.ground, steady_state.ground2, steady_state.ground3, steady_state.ground4, decel.ground]
air = [acel.air, steady_state.air1, steady_state.air2, steady_state.air1, steady_state.air2]
apex_reached = 0

def callback(data):
    global i, j, ref_height, startup, done, apex_reached
    global ser_R, ser_L, enc_1, enc_2, enc_3
    servoFeed_R = data.some_floats[0] 
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2] # Height
    encoder_2 = data.some_floats[3] # Length travled
    encoder_3 = data.some_floats[4]
    rad = d2r(encoder_1)
    
    test_boom()
    
    if startup:
        startup = False
        ref_height = np.sin(rad)*arm_len
        delay = time.time()*1000

        while time.time()*1000-delay <= 3000:
            acel.rest()
            send_message()

    # height = np.sin(rad)*arm_len - ref_height
    height = np.sin(rad)*arm_len

    print(i, j, apex_reached, height)
    if not firing:
        if not apex_reached:
            ground[i]()
        if apex_reached:
            air[j]()
    send_message()

    #250/1000
    if height<=140/1000 and apex_reached:
        if done:
            j += 1
            apex_reached = 0
            done = False
    if height>=140/1000 and not apex_reached and j<len(air):
        if done:
            i += 1
            apex_reached = 1
            done = False

    ser_R.append(servoFeed_R)
    ser_L.append(servoFeed_L)
    enc_1.append(encoder_1)
    enc_2.append(encoder_2)
    enc_3.append(encoder_3)

def listener():
    rp.Subscriber('sensor_data', my_message, callback)
    while not rp.core.is_shutdown():
        rp.rostime.wallsleep(0.5)


# main code_____________________________________________________________________
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    listener()
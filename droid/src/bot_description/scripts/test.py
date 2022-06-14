#!/usr/bin/env python3

from conda import CondaError
import numpy as np
import rospy as rp
import time
import pyautogui
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

dat[0] = np.pi/2 # Rev Right
dat[1] = np.pi/2 # Rev Left
dat[2] = 0 # Slider Right
dat[3] = 0 # Slider Left

def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)

def d2r(deg):
    return deg*np.pi/180

def r2d(rad):
    return rad*180/np.pi

def move(end, current):
    ratio = 0.1
    smootedMotion = ((1-ratio)*end) + (ratio*current)
    return smootedMotion

def test_boom():
    global firing, boom
    delay = time.time()*1000 - boom
    if delay<150:
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

ser_R = []
ser_L = []
enc_1 = []
enc_2 = []

# Callback code_________________________________________________________________________
max = 0
def callback(data):
    global ser_R, ser_L, enc_1, enc_2, startup, max
    servoFeed_R = data.some_floats[0] 
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2] # Height
    encoder_2 = data.some_floats[3] # Length travled    
    rad = d2r(encoder_1)

    # print('ass')
    if startup:
        startup = False
        delay = time.time()*1000

        while time.time()*1000-delay <= 3000:
            dat[0] = d2r(125)
            dat[1] = d2r(85)
            dat[2] = -1 # Slider Right
            dat[3] = -1 # Slider Left
            send_message()

    dat[2] = 1 # Slider Right
    dat[3] = -1 # Slider Left
    send_message()
    height = np.sin(rad)*arm_len
    if height>max:
        max = height
    print(max)

def listener():
    rp.Subscriber('sensor_data', my_message, callback)
    while not rp.core.is_shutdown():
        rp.rostime.wallsleep(0.5)


# main code_____________________________________________________________________
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    listener()
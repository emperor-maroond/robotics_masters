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
    file = open('data.csv', 'a')
    file.write('Servo Feedback Right:\n {}\n'.format(ser_R))
    file.write('Servo Feedback Left:\n {}\n'.format(ser_L))
    file.write('Encoder data 1:\n {}\n'.format(enc_1))
    file.write('Encoder data 2:\n {}\n'.format(enc_2))
    file.close()

    # data = np.asarray([[ser_R for n in range (0, len(ser_R))],
    #                 [ser_L for n in range (0, len(ser_L))],
    #                 [enc_1 for n in range (0, len(enc_1))],
    #                 [enc_2 for n in range (0, len(enc_2))]])
    # np.savetxt('data.txt', data)
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
def callback(data):
    global ser_R, ser_L, enc_1, enc_2, startup
    servoFeed_R = data.some_floats[0] 
    servoFeed_L = data.some_floats[1]
    encoder_1 = data.some_floats[2] # Height
    encoder_2 = data.some_floats[3] # Length travled    

    # print('ass')
    if startup:
        startup = False
        delay = time.time()*1000

        while time.time()*1000-delay <= 3000:
            dat[0] = 0 # Rev Right
            dat[1] = 0 # Rev Left
            dat[2] = -1 # Slider Right
            dat[3] = -1 # Slider Left
            send_message()

    dat[0] = np.pi
    dat[1] = np.pi 
    send_message()

    ser_R.append(servoFeed_R)
    ser_L.append(servoFeed_L)
    enc_1.append(encoder_1)
    enc_2.append(encoder_2)

def listener():
    rp.Subscriber('sensor_data', my_message, callback)
    while not rp.core.is_shutdown():
        rp.rostime.wallsleep(0.5)


# main code_____________________________________________________________________
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    listener()
#!/usr/bin/env python3

import numpy as np
import rospy as rp
import time
import signal
import sys

from std_msgs.msg import Float64
from gazebo_msgs.srv import GetLinkState, GetJointProperties, SpawnModel, DeleteModel

rp.init_node('commander')

pub_time = 5/1000
rate = rp.Rate(1/pub_time)


spawn = rp.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
delete = rp.ServiceProxy('/gazebo/delete_model', DeleteModel)

# Functions__________________________________________________________________________________
firing = False
boom = 0

link_states = rp.ServiceProxy( '/gazebo/get_link_state', GetLinkState)
joint_prop = rp.ServiceProxy( '/gazebo/get_joint_properties', GetJointProperties)

pub = [None]*4
pub[0] = rp.Publisher("/bot/RevR_position_controller/command", Float64, queue_size=1)
pub[1] = rp.Publisher("/bot/RevL_position_controller/command", Float64, queue_size=1)
pub[2] = rp.Publisher("/bot/SliderR_position_controller/command", Float64, queue_size=1)
pub[3] = rp.Publisher("/bot/SliderL_position_controller/command", Float64, queue_size=1)

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
    file.write('Rime:\n {}\n'.format(tims))
    file.close()

    acel.rest()
    send_message()
    print ('KeyboardInterrupt is caught')
    sys.exit(0)

def d2r(deg):
    return deg*np.pi/190

def r2d(rad):
    return rad*190/np.pi

def move(end, current):
    ratio = 0.01
    smootedMotion = ((1-ratio)*end) + (ratio*current)
    return smootedMotion

def test_boom():
    global firing, boom
    delay = time.time()*1000 - boom
    if delay<120:
        firing = True
    else:
        firing = False

def send_message():
    global message
    # rp.loginfo(message)
    for i in range(0, len(dat)):
        pub[i].publish(dat[i])
    
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
tims = []

class acel():
    def rest():
        end_R = d2r(70)
        end_L = d2r(110)
        dat[0] = end_R
        dat[1] = end_L
        dat[2] = -190
        dat[3] = -190

    def ground():
        global done
        end_R = d2r(70)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = 190
            done = True

    def air():
        global done
        dat[2] = -190
        dat[3] = -190
        end_R = d2r(110)
        end_L = d2r(70)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = -190
            done = True

class steady_state():
    def ground():
        global done, i, boom
        end_R = d2r(110)
        end_L = d2r(70)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = -190
            i += 1
            boom = time.time()*1000

    def ground2():
        global done
        end_R = d2r(110)
        end_L = d2r(70)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = 190
            dat[3] = -190
            done = True

    def air1():
        global done
        dat[2] = -190
        dat[3] = -190
        end_R = d2r(70)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = -190
            done = True

    def ground3():
        global done, i, boom
        end_R = d2r(70)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = -190
            i += 1
            boom = time.time()*1000

    def ground4():
        global done
        end_R = d2r(70)
        end_L = d2r(110)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = 190
            done = True

    def air2():
        global done
        dat[2] = -190
        dat[3] = -190
        end_R = d2r(110)
        end_L = d2r(70)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = -190
            done = True

class decel():
    def ground():
        global done
        end_R = d2r(110)
        end_L = d2r(70)
        dat[0] = move(end_R, dat[0])
        dat[1] = move(end_L, dat[1])
        if round(dat[0], 5)==round(end_R, 5) and round(dat[1], 5)==round(end_L, 5):
            dat[2] = -190
            dat[3] = -190
            done = True
        

# Callback code_________________________________________________________________________
ground = [acel.ground, steady_state.ground, steady_state.ground2, steady_state.ground3, steady_state.ground4, steady_state.ground, steady_state.ground2, steady_state.ground3, steady_state.ground4, decel.ground]
air = [acel.air, steady_state.air1, steady_state.air2, steady_state.air1, steady_state.air2]
apex_reached = 0

def callback():
    while not rp.core.is_shutdown():
        global i, j, startup, done, apex_reached
        global ser_R, ser_L, enc_1, enc_2, enc_3
        servoFeed_R = 0
        servoFeed_L = 0
        encoder_1 = 0
        encoder_2 = 0
        encoder_3 = 0
        
        test_boom()
        
        if startup:
            startup = False
            delay = time.time()*1000
            while time.time()*1000-delay <= 3000:
                acel.rest()
                send_message()

        links = link_states("base_link","")
        linksR = joint_prop("RevR")
        linksL = joint_prop("RevL")
        body_angle = joint_prop('rotation')
        # height = links.pose.position.z
        height = links.link_state.pose.position.z + 0.2344030309035076

        # print(i, j, apex_reached, height)
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

        servoFeed_R = linksR.position
        servoFeed_L = linksL.position
        encoder_1 = height
        encoder_2 = links.link_state.pose.position.y
        encoder_3 = body_angle.position
        tim = time.time()
        ser_R.append(servoFeed_R)
        ser_L.append(servoFeed_L)
        enc_1.append(encoder_1) 
        enc_2.append(encoder_2)
        enc_3.append(encoder_3)
        tims.append(tim)

# main code_____________________________________________________________________
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    callback()
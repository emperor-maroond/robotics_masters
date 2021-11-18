#!/usr/bin/env python3

import numpy as np
import rospy as rp
import time

from math import isclose
from std_msgs.msg import Float64
from std_srvs.srv import Empty
from gazebo_msgs.msg import ModelStates

rp.init_node('commander')

pub_time = 10/1000
rate = rp.Rate(1/pub_time)

reset_simulation = rp.ServiceProxy('/gazebo/reset_simulation', Empty)

pub = [None]*4

pub[0] = rp.Publisher("/bot/RevR_position_controller/command", Float64, queue_size=10)
pub[1] = rp.Publisher("/bot/RevL_position_controller/command", Float64, queue_size=10)
pub[2] = rp.Publisher("/bot/SliderR_position_controller/command", Float64, queue_size=10)
pub[3] = rp.Publisher("/bot/SliderL_position_controller/command", Float64, queue_size=10)

# Functions__________________________________________________________________________________
firing = False
boom = 0
def d2r(deg):
    return deg*np.pi/165

def r2d(rad):
    return rad*165/np.pi

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
    if delay<150:
        # print(delay)
        firing = True
    else:
        firing = False

# States_____________________________________________________________________________________
flag = 1
done = 0
start_R = 0
end_R   = 0
start_L = 0
end_L   = 0
z = 1

def state_0():  # START state as well as STOP state
    global end_R, end_L, done
    end_R = d2r(90+30)
    end_L = d2r(90-30)
    pub[0].publish(end_R)
    pub[1].publish(end_L)
    pub[2].publish(-165)
    pub[3].publish(-165)
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
        end_R = d2r(90+30)
        end_L = d2r(90-45)
        pub[2].publish(-165)
        pub[3].publish(-165)
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        if R==end_R and L==end_L:
            # print("fuck 1")
            pub[2].publish(165)
            if not done:
                boom = time.time()*1000
            z = 0
            done = 1
    pub[0].publish(R)
    pub[1].publish(L)


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
        end_R = d2r(90+30)
        end_L = d2r(90-0)
        pub[2].publish(-165)
        pub[3].publish(-165)        
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        if R==end_R and L==end_L:
            # print("fuck 2")
            z = 0
            pub[3].publish(165)
            print(r2d(L))
            if not done:
                boom = time.time()*1000
            done = 1
    pub[0].publish(R)
    pub[1].publish(L)


def state_3():
    global flag, start_R, end_R, start_L, end_L, z, done, boom
    if flag:
        global R, L
        done = 0
        R = end_R
        L = end_L  
        flag = 0
        start_R = end_R
        start_L = end_L
        end_R = d2r(90-30)
        end_L = d2r(90+30)        
        pub[2].publish(-165)
        pub[3].publish(165)        
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        if R==end_R and L==end_L:
            z = 0
            pub[3].publish(-165)
            done = 1
            # print("done")
    pub[0].publish(R)
    pub[1].publish(L)

def state_4():
    global flag, start_R, end_R, start_L, end_L, z, done, boom
    if flag:
        done = 0
        global R, L
        R = end_R
        L = end_L
        flag = 0
        start_R = end_R
        start_L = end_L
        end_R = d2r(90-45)
        end_L = d2r(90+30)
        pub[2].publish(-165)
        pub[3].publish(-165)
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        if R==end_R and L==end_L:
            pub[3].publish(165)
            if not done:
                boom = time.time()*1000
            z = 0
            done = 1
    pub[0].publish(R)
    pub[1].publish(L)

def state_5():
    global flag, start_R, end_R, start_L, end_L, z, done, boom
    if flag:
        global R, L
        done = 0
        R = end_R
        L = end_L  
        flag = 0
        start_R = end_R
        start_L = end_L
        end_R = d2r(90-30)
        end_L = d2r(90+30)  
        pub[2].publish(-165)
        pub[3].publish(-165)        
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        if R==end_R and L==end_L:
            z = 0
            pub[2].publish(165)
            if not done:
                boom = time.time()*1000
            done = 1
            # print("fuck 5")
    pub[0].publish(R)
    pub[1].publish(L)

def state_6():
    global flag, start_R, end_R, start_L, end_L, z, done, boom
    if flag:
        global R, L
        done = 0
        R = end_R
        L = end_L  
        flag = 0
        start_R = end_R
        start_L = end_L
        end_R = d2r(90+30)
        end_L = d2r(90-30)  
        pub[2].publish(165)
        pub[3].publish(-165)        
    if not flag:
        z += 1
        if L!=end_L:
            L = move(start_L, end_L, z)
        if R!=end_R:
            R = move(start_R, end_R, z)
        else:
            pub[2].publish(-165)
            z = 0
            done = 1
    pub[0].publish(R)
    pub[1].publish(L)

i = 0
ground = False
apex = False
run = True
states = [state_0, state_1, state_2, state_3, state_4, state_5, state_6]
def callback(data):
    global i, apex, flag, ground, run, done
    pose = data.pose[2]
    z = pose.position.z
    # print(z)
    # print(run)
    test_boom()
    if run:
        states[i]()
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
        if z<-0.22:
            if i==0 and not ground:
                flag = 1
            elif not ground:
                run = True
                flag = 1
        if z>-0.16 and not apex:
            if not apex and ground and i>0:
                run = True
                flag = 1
        if z>-0.22 and z and apex:
            # print(ground, apex, done)
            if ground and apex and i>0:
                # print(i)
                run = True
                flag = 1
    if i >= len(states)-1:
        i = len(states)-1
        # print("NO", z)
    # print(i)


def listener():
    try:
        rp.Subscriber('/gazebo/link_states', ModelStates, callback)
        while not rp.core.is_shutdown():
            rp.rostime.wallsleep(0.5)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    reset_simulation()
    time.sleep(0.5)
    states[0]()
    rp.sleep(1)  
    listener()
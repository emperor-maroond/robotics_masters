#!/usr/bin/env python3

import numpy as np
import rospy as rp
import time

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

tyme = 0
def callback(data):
    global tyme
    pose = data.pose[2]
    z = pose.position.z
    # z = np.round(z, 5)
    pub[0].publish(90*np.pi/180)
    pub[1].publish(90*np.pi/180)
    # print(z)

    if(z<-0.22):
        tyme = np.round(time.time()*1000)
        pub[2].publish(170)
        pub[3].publish(170)
    delay = np.round(time.time()*1000) - tyme
    if(z>-0.22 and delay>200):
        print(delay)
        pub[2].publish(-170)
        pub[3].publish(-170)


def listener():
    try:
        rp.Subscriber('/gazebo/link_states', ModelStates, callback)
        while not rp.core.is_shutdown():
            rp.rostime.wallsleep(0.5)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    reset_simulation()
    pub[2].publish(-170)
    pub[3].publish(-170)
    time.sleep(2)
    listener()
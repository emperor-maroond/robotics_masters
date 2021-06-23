#!/usr/bin/env python3

import numpy as np
import rospy as rp
import cloudpickle
import time

from std_msgs.msg import Float64
from std_srvs.srv import Empty

rp.init_node('commander')

reset_simulation = rp.ServiceProxy('/gazebo/reset_simulation', Empty)

pub = [None]*4

pub[0] = rp.Publisher("/bot/RevR_position_controller/command", Float64, queue_size=10)
pub[1] = rp.Publisher("/bot/RevL_position_controller/command", Float64, queue_size=10)
pub[2] = rp.Publisher("/bot/SliderR_position_controller/command", Float64, queue_size=10)
pub[3] = rp.Publisher("/bot/SliderL_position_controller/command", Float64, queue_size=10)

data = [None]*3

with open("accel.bin", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("steady-state.bin", "rb") as f:
    data[1] = cloudpickle.load(f)      

with open("decel.bin", "rb") as f:
    data[2] = cloudpickle.load(f)

N = data[1].N[-1]
if __name__ == '__main__': 
    reset_simulation()

    pub[0].publish(data[0].q0[1, 'theta_l_R'].value - np.pi/2)
    pub[1].publish(data[0].q0[1, 'theta_l_L'].value - np.pi/2)
    pub[2].publish(-data[0].F_max)
    pub[3].publish(-data[0].F_max)

    time.sleep(2)

    for i in range(0, len(data)):
        for n in range(1, N+1):
            pub[0].publish(data[i].q0[n, 'theta_l_R'].value - np.pi/2)
            pub[1].publish(data[i].q0[n, 'theta_l_L'].value - np.pi/2)
            F = data[i].F_max*(data[i].Fbang_pos_R[n].value - data[i].Fbang_neg_R[n].value)
            pub[2].publish(F)
            F = data[i].F_max*(data[i].Fbang_pos_L[n].value - data[i].Fbang_neg_L[n].value)
            pub[3].publish(F)
            
            sleep = data[i].h[n].value
            rp.sleep(sleep)
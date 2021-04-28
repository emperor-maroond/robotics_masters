import numpy as np
import rospy as rp

from std_msgs.msg import Float64

rp.init_node('commander')

pub = [None]*4

pub[0] = rp.Publisher("/bot/RevR_position_controller/command", Float64, queue_size=10)
pub[1] = rp.Publisher("/bot/RevL_position_controller/command", Float64, queue_size=10)
pub[2] = rp.Publisher("/bot/SliderR_position_controller/command", Float64, queue_size=10)
pub[3] = rp.Publisher("/bot/SliderL_position_controller/command", Float64, queue_size=10)

data = np.load('data.npy', allow_pickle=True)
#print(data[1][0])

'''data = asarray([[N],                                                         0
                [m.tau_a_L[n].value for n in range (1, N+1)],                   1
                [m.Fbang_pos_L[n].value for n in range (1, N+1)],               2
                [m.Fbang_neg_L[n].value for n in range (1, N+1)],               3
                [m.FhardStop_ext_L[n].value for n in range (1, N+1)],           4
                [m.FhardStop_rtn_L[n].value for n in range (1, N+1)],           5
                [m.q0[n,'theta_l_L'].value for n in range (1, N+1)],            6   
                [m.q0[n,'r_L'].value for n in range (1, N+1)],                  7
                [m.tau_a_R[n].value for n in range (1, N+1)],                   8
                [m.Fbang_pos_R[n].value for n in range (1, N+1)],               9
                [m.Fbang_neg_R[n].value for n in range (1, N+1)],               10
                [m.FhardStop_ext_R[n].value for n in range (1, N+1)],           11
                [m.FhardStop_rtn_R[n].value for n in range (1, N+1)],           12     
                [m.q0[n,'theta_l_R'].value for n in range (1, N+1)],            13
                [m.q0[n,'r_R'].value for n in range (1, N+1)],                  14
                [m.q0[n,'x'].value for n in range (1, N+1)],                    15
                [m.q0[n,'z'].value for n in range (1, N+1)],                    16
                [m.damping],                                                    17
                [m.F_max]])                                                     18'''

N = data[0][0]

if __name__ == '__main__': 
    for n in range(1, N):
        pub[0].publish(data[8][n])
        pub[1].publish(data[1][n])
        pub[2].publish(data[18][0]*(data[9][n] - data[10][n]))
        pub[3].publish(data[18][0]*(data[2][n] - data[3][n]))
        rp.sleep(0.1)
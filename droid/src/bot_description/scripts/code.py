import numpy as np
import rospy as rp

from std_msgs.msg import Float64

pub = [4]

pub[0] = rp.Publisher("/bot/RevR_position_controller/command", Float64, queue_size=10)
pub[1] = rp.Publisher("/bot/RevL_position_controller/command", Float64, queue_size=10)
pub[2] = rp.Publisher("/bot/SliderR_position_controller/command", Float64, queue_size=10)
pub[3] = rp.Publisher("/bot/SliderL_position_controller/command", Float64, queue_size=10)

data = np.load('data.npy')

print(data)

if __name__ == '__main__': 
    for n in range(100):
        pass    
    pass
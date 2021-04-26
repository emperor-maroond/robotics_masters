import numpy as np
import rospy as rp

from std_msgs.msg import Float64

pub = rp.Publisher("")

data = np.load('data.npy')

print(data)

if __name__ == '__main__': 
    pass
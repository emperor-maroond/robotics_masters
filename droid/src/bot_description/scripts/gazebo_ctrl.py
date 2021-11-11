#!/usr/bin/env python3

import numpy as np
import rospy as rp
import time

from std_msgs.msg import Float64
from std_srvs.srv import Empty
from gazebo_msgs.msg import ModelStates
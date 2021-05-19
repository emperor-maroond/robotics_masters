import numpy as np
import cloudpickle

data = [None]*3

with open("accel.pkl", "rb") as f:
    data[0] = cloudpickle.load(f)

with open("steady-state.pkl", "rb") as f:
    data[1] = cloudpickle.load(f)      

with open("decel.pkl", "rb") as f:
    data[2] = cloudpickle.load(f)

N = data[1].N[-1]
for n in range(1, N+1):
    print(data[1].q0[n, 'x'].value)
    
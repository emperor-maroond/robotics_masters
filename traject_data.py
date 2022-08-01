import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cloudpickle

m = [0]*3
# damp_x3 has right shape but is way faster than actual robot
with open("Optimisation_Code/Feasible_Solution/damp_x3/steady-state.pkl", "rb") as f:
    m[1] = cloudpickle.load(f)
    
with open("Optimisation_Code/Feasible_Solution/damp_x3/accel.pkl", "rb") as f:
    m[0] = cloudpickle.load(f)
    
with open("Optimisation_Code/Feasible_Solution/damp_x3/decel.pkl", "rb") as f:
    m[2] = cloudpickle.load(f)

N = m[0].N[-1]
cN = m[0].cN[-1]
dt = 5/1000

# Handel the optimiser data___________________________________________________________________________________________________
N_time = []
cN_time = []
cN_adder = 0
adder = 0
for i in range(0, 3): # Add the cN node time into an array
    if(i>0):
        cN_adder += (m[i-1].tt0[N].value - m[i-1].tt0[1].value)
    for n in range(1, N+1):
        for c in range(1, cN+1):
            cN_time.append(m[i].tt[n,c].value - m[i].tt[1,1].value + cN_adder)
            
for i in range(0, 3): # Add the N node time into an array
    if(i>0):
        adder += (m[i-1].tt0[N].value - m[i-1].tt0[1].value)
    for n in range(1, N+1):
        N_time.append(m[i].tt0[n].value - m[i].tt0[1].value + adder)

x_tmp = []
z_tmp = []
r_tmp = []
l_tmp = []
adder = 0
for i in range(0, 3):
    if(i>0):
        adder += m[i-1].q[N,cN,'x'].value
    for n in range(1, N+1):
        for c in range(1, cN+1):
            z_tmp.append(m[i].q[n,c,'z'].value)
            x_tmp.append(m[i].q[n,c,'x'].value + adder) 
            r_tmp.append(m[i].q[n,c,'theta_l_R'].value*180/np.pi)
            l_tmp.append(m[i].q[n,c,'theta_l_L'].value*180/np.pi)

def interpolate(y_inter, cur_time, x_inter, position):
    ans = 0
    for i in range(position, len(x_inter)):
        if(x_inter[i]<=cur_time and cur_time<x_inter[i+1]):
            position = i
            ans = y_inter[i] + (cur_time - x_inter[i])*(y_inter[i+1] - y_inter[i])/(x_inter[i+1] - x_inter[i])
            return ans, position

run_time = 0
pub_time = 1/1000
position_cN = 0
x = []
z = []
r = []
l = []
time = []
while 1:
    if(run_time>cN_time[-1]):
        break
    
    tmp, position_cN = interpolate(x_tmp, run_time, cN_time, position_cN)
    x.append(tmp)

    tmp, position_cN = interpolate(z_tmp, run_time, cN_time, position_cN)
    z.append(tmp)

    run_time += pub_time
    time.append(run_time)     

plt.figure(1)
# plt.xticks(np.arange(start=0, stop=len(z1)*dt, step=0.5))
plt.ylabel('vertical distance (m)')
plt.xlabel('time(s)')
plt.plot(time, z, LineWidth=1)
plt.plot(cN_time, z_tmp, LineWidth=1)
plt.legend()

plt.show()
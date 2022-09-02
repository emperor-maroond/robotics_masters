import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cloudpickle
from scipy.interpolate import interp1d

m1 = [] # 0.7 m/s SS
with open("Optimisation_Code/Feasible_Solution/01/steady-state.pkl", "rb") as f:
    m1.append(cloudpickle.load(f))    
# with open("Optimisation_Code/Feasible_Solution/02/accel.pkl", "rb") as f:
#     m1.append(cloudpickle.load(f))  
# with open("Optimisation_Code/Feasible_Solution/02/decel.pkl", "rb") as f:
#     m1.append(cloudpickle.load(f)) 

m2 = [] # 0.5 m/s SS
with open("Optimisation_Code/Feasible_Solution/00/steady-state.pkl", "rb") as f:
    m2.append(cloudpickle.load(f))    
# with open("Optimisation_Code/Feasible_Solution/00/accel.pkl", "rb") as f:
#     m2.append(cloudpickle.load(f)) 
# with open("Optimisation_Code/Feasible_Solution/00/decel.pkl", "rb") as f:
#     m2.append(cloudpickle.load(f)) 

m3 = [] # 1.0 m/s SS
with open("Optimisation_Code/Feasible_Solution/02/steady-state.pkl", "rb") as f:
    m3.append(cloudpickle.load(f))   
# with open("Optimisation_Code/Feasible_Solution/03/accel.pkl", "rb") as f:
#     m3.append(cloudpickle.load(f))  
# with open("Optimisation_Code/Feasible_Solution/03/decel.pkl", "rb") as f:
#     m3.append(cloudpickle.load(f)) 

N1 = m1[0].N[-1]
cN1 = m1[0].cN[-1]

N2 = m2[0].N[-1]
cN2 = m2[0].cN[-1]

N3 = m3[0].N[-1]
cN3 = m3[0].cN[-1]
dt = 1/1000

# Handel the optimiser data___________________________________________________________________________________________________
N_time1 = []
cN_time1 = []
cN_adder1 = 0
adder1 = 0
for i in range(0, len(m1)): # Add the cN node time into an array
    if(i>0):
        cN_adder1 += (m1[i-1].tt0[N1].value - m1[i-1].tt0[1].value)
    for n in range(1, N1+1):
        for c in range(1, cN1+1):
            cN_time1.append(m1[i].tt[n,c].value - m1[i].tt[1,1].value + cN_adder1)
            
for i in range(0, len(m1)): # Add the N node time into an array
    if(i>0):
        adder1 += (m1[i-1].tt0[N1].value - m1[i-1].tt0[1].value)
    for n in range(1, N1+1):
        N_time1.append(m1[i].tt0[n].value - m1[i].tt0[1].value + adder1)

x1 = []
z1 = []
r1 = []
l1 = []
vel_z1 = []
vel_x1 = []
GRF_L1 = []
GRF_R1 = []
adder = 0
for i in range(0, len(m1)):
    if(i>0):
        adder += m1[i-1].q[N1,cN1,'x'].value
    for n in range(1, N1+1):
        for c in range(1, cN1+1):
            z1.append(m1[i].q[n,c,'z'].value)
            vel_z1.append(m1[i].dq[n,c,'z'].value)
            vel_x1.append(m1[i].dq[n,c,'x'].value)
            x1.append(m1[i].q[n,c,'x'].value + adder) 
            r1.append(m1[i].q[n,c,'theta_l_R'].value*180/np.pi)
            l1.append(m1[i].q[n,c,'theta_l_L'].value*180/np.pi)
            GRF_L1.append(m1[i].GRF_L[n,c,'Z','ps'].value)
            GRF_R1.append(m1[i].GRF_R[n,c,'Z','ps'].value)

N_time2 = []
cN_time2 = []
cN_adder2 = 0
adder2 = 0
for i in range(0, len(m2)): # Add the cN node time into an array
    if(i>0):
        cN_adder2 += (m2[i-1].tt0[N2].value - m2[i-1].tt0[1].value)
    for n in range(1, N2+1):
        for c in range(1, cN2+1):
            cN_time2.append(m2[i].tt[n,c].value - m2[i].tt[1,1].value + cN_adder2)
            
for i in range(0, len(m2)): # Add the N node time into an array
    if(i>0):
        adder2 += (m2[i-1].tt0[N2].value - m2[i-1].tt0[1].value)
    for n in range(1, N2+1):
        N_time2.append(m2[i].tt0[n].value - m2[i].tt0[1].value + adder2)

x2 = []
z2 = []
r2 = []
l2 = []
vel_z2 = []
vel_x2 = []
GRF_L2 = []
GRF_R2 = []
adder = 0
for i in range(0, len(m2)):
    if(i>0):
        adder += m2[i-1].q[N2,cN2,'x'].value
    for n in range(1, N2+1):
        for c in range(1, cN2+1):
            z2.append(m2[i].q[n,c,'z'].value)
            vel_z2.append(m2[i].dq[n,c,'z'].value)
            x2.append(m2[i].q[n,c,'x'].value + adder) 
            vel_x2.append(m2[i].dq[n,c,'x'].value)
            r2.append(m2[i].q[n,c,'theta_l_R'].value*180/np.pi)
            l2.append(m2[i].q[n,c,'theta_l_L'].value*180/np.pi)
            GRF_L2.append(m2[i].GRF_L[n,c,'Z','ps'].value)
            GRF_R2.append(m2[i].GRF_R[n,c,'Z','ps'].value)

N_time3 = []
cN_time3 = []
cN_adder3 = 0
adder3 = 0
for i in range(0, len(m3)): # Add the cN node time into an array
    if(i>0):
        cN_adder3 += (m3[i-1].tt0[N3].value - m3[i-1].tt0[1].value)
    for n in range(1, N3+1):
        for c in range(1, cN3+1):
            cN_time3.append(m3[i].tt[n,c].value - m3[i].tt[1,1].value + cN_adder3)
            
for i in range(0, len(m3)): # Add the N node time into an array
    if(i>0):
        adder3 += (m3[i-1].tt0[N3].value - m3[i-1].tt0[1].value)
    for n in range(1, N3+1):
        N_time3.append(m3[i].tt0[n].value - m3[i].tt0[1].value + adder3)

x3 = []
z3 = []
r3 = []
l3 = []
vel_z3 = []
vel_x3 = []
GRF_L3 = []
GRF_R3 = []
adder = 0
for i in range(0, len(m3)):
    if(i>0):
        adder += m3[i-1].q[N3,cN3,'x'].value
    for n in range(1, N3+1):
        for c in range(1, cN3+1):
            z3.append(m3[i].q[n,c,'z'].value)
            vel_z3.append(m3[i].dq[n,c,'z'].value)
            x3.append(m3[i].q[n,c,'x'].value + adder)
            vel_x3.append(m3[i].dq[n,c,'x'].value) 
            r3.append(m3[i].q[n,c,'theta_l_R'].value*180/np.pi)
            l3.append(m3[i].q[n,c,'theta_l_L'].value*180/np.pi)
            GRF_L3.append(m3[i].GRF_L[n,c,'Z','ps'].value)
            GRF_R3.append(m3[i].GRF_R[n,c,'Z','ps'].value)

# The graphs__________________________________________________________________________________________________

plt.figure(1)
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.2), fontsize=18)
plt.ylabel('vertical height (m)', fontsize=22)
plt.xlabel('time (s)', fontsize=22)
plt.plot(cN_time2, z2, linewidth=1.5, label='0.5 m/s')
plt.plot(cN_time1, z1, linewidth=1.5, label='0.7 m/s')
plt.plot(cN_time3, z3, linewidth=1.5, label='0.9 m/s')
plt.grid()
plt.legend(fontsize=15) 

plt.figure(2)
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.2), fontsize=18)
plt.ylabel('vertical velocity (m/s)', fontsize=22)
plt.xlabel('time (s)', fontsize=22)
plt.plot(cN_time2, vel_z2, linewidth=1.5, label='0.5 m/s')
plt.plot(cN_time1, vel_z1, linewidth=1.5, label='0.7 m/s')
plt.plot(cN_time3, vel_z3, linewidth=1.5, label='0.9 m/s')
plt.grid()
plt.legend(fontsize=15)

plt.figure(3)
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.2), fontsize=18)
plt.ylabel('horisontal distance (m)', fontsize=22)
plt.xlabel('time (s)', fontsize=22)
plt.plot(cN_time2, x2, linewidth=1.5, label='0.5 m/s')
plt.plot(cN_time1, x1, linewidth=1.5, label='0.7 m/s')
plt.plot(cN_time3, x3, linewidth=1.5, label='0.9 m/s')
plt.grid()
plt.legend(fontsize=15) 

plt.figure(4)
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.2), fontsize=18)
plt.ylabel('horisontal velocity (m/s)', fontsize=22)
plt.xlabel('time (s)', fontsize=22)
plt.plot(cN_time2, vel_x2, linewidth=1.5, label='0.5 m/s')
plt.plot(cN_time1, vel_x1, linewidth=1.5, label='0.7 m/s')
plt.plot(cN_time3, vel_x3, linewidth=1.5, label='0.9 m/s')
plt.grid()
plt.legend(fontsize=15)

# plt.figure(5)
# plt.yticks(fontsize=18)
# plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.2), fontsize=18)
# plt.ylabel('GRF (N)', fontsize=22)
# plt.xlabel('time (s)', fontsize=22)
# plt.plot(cN_time2, GRF_L2, linewidth=1.5, c='blue', label='0.5 m/s')
# plt.plot(cN_time2, GRF_R2, linewidth=1.5, c='blue', linestyle='dotted')
# plt.plot(cN_time1, GRF_L1, linewidth=1.5, c='r', label='0.7 m/s')
# plt.plot(cN_time1, GRF_R1, linewidth=1.5, c='r', linestyle='dotted')
# plt.plot(cN_time3, GRF_L3, linewidth=1.5, c='g', label='0.9 m/s')
# plt.plot(cN_time3, GRF_R3, linewidth=1.5, c='g', linestyle='dotted')
# plt.grid()
# plt.legend(fontsize=15)

plt.show()
# avg = 0
# for n in range(1, N1+1):
#     avg += m3[0].dq0[n, 'x'].value

# print(avg/N1)

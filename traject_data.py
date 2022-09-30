from traceback import print_tb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cloudpickle
from scipy.interpolate import interp1d

m1 = [] # 0.7 m/s SS
with open("Optimisation_Code/Feasible_Solution/damp_x1/steady-state.pkl", "rb") as f:
    m1.append(cloudpickle.load(f))    
# with open("Optimisation_Code/Feasible_Solution/02/accel.pkl", "rb") as f:
#     m1.append(cloudpickle.load(f))  
# with open("Optimisation_Code/Feasible_Solution/02/decel.pkl", "rb") as f:
#     m1.append(cloudpickle.load(f)) 

m2 = [] # 0.28 m/s SS
with open("Optimisation_Code/Feasible_Solution/damp_x2/steady-state.pkl", "rb") as f:
    m2.append(cloudpickle.load(f))    
# with open("Optimisation_Code/Feasible_Solution/00/accel.pkl", "rb") as f:
#     m2.append(cloudpickle.load(f)) 
# with open("Optimisation_Code/Feasible_Solution/00/decel.pkl", "rb") as f:
#     m2.append(cloudpickle.load(f)) 

m3 = [] # 1.0 m/s SS
with open("Optimisation_Code/Feasible_Solution/damp_x3/steady-state.pkl", "rb") as f:
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
            cN_time1.append((m1[i].tt[n,c].value - m1[i].tt[1,1].value + cN_adder1) * 1.0)
            
for i in range(0, len(m1)): # Add the N node time into an array
    if(i>0):
        adder1 += (m1[i-1].tt0[N1].value - m1[i-1].tt0[1].value)
    for n in range(1, N1+1):
        N_time1.append((m1[i].tt0[n].value - m1[i].tt0[1].value + adder1)*1.0)

x1 = []
z1 = []
r1 = []
l1 = []
vel_z1 = []
vel_x1 = []
grf_L1 = []
grf_R1 = []
F_pos_L1 = []
F_neg_L1 = []
F_pos_R1 = []
F_neg_R1 = []
adder = 0
for i in range(0, len(m1)):
    if(i>0):
        adder += m1[i-1].q[N1,cN1,'x'].value
    for n in range(1, N1+1):
        for c in range(1, cN1+1):
            z1.append(m1[i].q[n,c,'z'].value)
            vel_z1.append(m1[i].dq[n,c,'z'].value)
            vel_x1.append(m1[i].dq[n,c,'x'].value * (100-0)/100)
            x1.append(m1[i].q[n,c,'x'].value + adder) 
            r1.append(m1[i].q[n,c,'theta_l_R'].value)
            l1.append(m1[i].q[n,c,'theta_l_L'].value)
            grf_L1.append(m1[i].GRF_L[n,c,'Z','ps'].value)
            grf_R1.append(m1[i].GRF_R[n,c,'Z','ps'].value)
            F_pos_L1.append(m1[i].Fbang_pos_L[n].value)
            F_neg_L1.append(m1[i].Fbang_neg_L[n].value)
            F_pos_R1.append(m1[i].Fbang_pos_R[n].value)
            F_neg_R1.append(m1[i].Fbang_neg_R[n].value)

N_time2 = []
cN_time2 = []
cN_adder2 = 0
adder2 = 0
for i in range(0, len(m2)): # Add the cN node time into an array
    if(i>0):
        cN_adder2 += (m2[i-1].tt0[N2].value - m2[i-1].tt0[1].value)
    for n in range(1, N2+1):
        for c in range(1, cN2+1):
            cN_time2.append((m2[i].tt[n,c].value - m2[i].tt[1,1].value + cN_adder2) * 1.0)
            
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
grf_L2 = []
grf_R2 = []
F_pos_L2 = []
F_neg_L2 = []
F_pos_R2 = []
F_neg_R2 = []
adder = 0
for i in range(0, len(m2)):
    if(i>0):
        adder += m2[i-1].q[N2,cN2,'x'].value
    for n in range(1, N2+1):
        for c in range(1, cN2+1):
            z2.append(m2[i].q[n,c,'z'].value)
            vel_z2.append(m2[i].dq[n,c,'z'].value)
            x2.append(m2[i].q[n,c,'x'].value + adder) 
            vel_x2.append(m2[i].dq[n,c,'x'].value * (100-0)/100)
            r2.append(m2[i].q[n,c,'theta_l_R'].value)
            l2.append(m2[i].q[n,c,'theta_l_L'].value)
            grf_L2.append(m2[i].GRF_L[n,c,'Z','ps'].value)
            grf_R2.append(m2[i].GRF_R[n,c,'Z','ps'].value)
            F_pos_L2.append(m2[i].Fbang_pos_L[n].value)
            F_neg_L2.append(m2[i].Fbang_neg_L[n].value)
            F_pos_R2.append(m2[i].Fbang_pos_R[n].value)
            F_neg_R2.append(m2[i].Fbang_neg_R[n].value)

N_time3 = []
cN_time3 = []
cN_adder3 = 0
adder3 = 0
for i in range(0, len(m3)): # Add the cN node time into an array
    if(i>0):
        cN_adder3 += (m3[i-1].tt0[N3].value - m3[i-1].tt0[1].value)
    for n in range(1, N3+1):
        for c in range(1, cN3+1):
            cN_time3.append((m3[i].tt[n,c].value - m3[i].tt[1,1].value + cN_adder3) * 1.0)
            
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
grf_L3 = []
grf_R3 = []
F_pos_L3 = []
F_neg_L3 = []
F_pos_R3 = []
F_neg_R3 = []
adder = 0
for i in range(0, len(m3)):
    if(i>0):
        adder += m3[i-1].q[N3,cN3,'x'].value
    for n in range(1, N3+1):
        for c in range(1, cN3+1):
            z3.append(m3[i].q[n,c,'z'].value)
            vel_z3.append(m3[i].dq[n,c,'z'].value)
            x3.append(m3[i].q[n,c,'x'].value + adder)
            vel_x3.append(m3[i].dq[n,c,'x'].value * (100-0)/100) 
            r3.append(m3[i].q[n,c,'theta_l_R'].value)
            l3.append(m3[i].q[n,c,'theta_l_L'].value)
            grf_L3.append(m3[i].GRF_L[n,c,'Z','ps'].value)
            grf_R3.append(m3[i].GRF_R[n,c,'Z','ps'].value)
            F_pos_L3.append(m3[i].Fbang_pos_L[n].value)
            F_neg_L3.append(m3[i].Fbang_neg_L[n].value)
            F_pos_R3.append(m3[i].Fbang_pos_R[n].value) 
            F_neg_R3.append(m3[i].Fbang_neg_R[n].value)

# The graphs__________________________________________________________________________________________________

plt.figure(1)
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.4), fontsize=18)
plt.ylabel('vertical height (m)', fontsize=22)
plt.xlabel('time (s)', fontsize=22)
plt.plot(cN_time1, z1, linewidth=1.5, label='0.40 m/s')
boom = True
bang = False
for i in range(0, len(F_pos_L1)):
    if F_pos_L1[i]>0.7 and boom:
        boom = False
        plt.plot(cN_time1[i], z1[i], c='k', marker='+', markersize='14')
    if F_neg_L1[i]>0.5 and not boom:
        boom = True
        plt.plot(cN_time1[i], z1[i], c='k', marker='.', markersize='12')
    if F_pos_R1[i]>0.5 and bang:
        bang = False
        plt.plot(cN_time1[i], z1[i], c='r', marker='x', markersize='14')
    if F_neg_R1[i]>0.5 and not bang:
        bang = True
        plt.plot(cN_time1[i], z1[i], c='r', marker='.', markersize='12')
plt.grid()
plt.legend(fontsize=15) 

plt.figure(2)
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.4), fontsize=18)
plt.ylabel('vertical height (m)', fontsize=22)
plt.xlabel('time (s)', fontsize=22)
plt.plot(cN_time2, z2, linewidth=1.5, label='0.15 m/s')
boom = False
bang = True
for i in range(0, len(F_pos_L2)):
    if F_pos_L2[i]>0.6 and boom:
        boom = False
        plt.plot(cN_time2[i], z2[i], c='k', marker='+', markersize='14')
    if F_neg_L2[i]>0.6 and not boom:
        boom = True
        plt.plot(cN_time2[i], z2[i], c='k', marker='.', markersize='12')
    if F_pos_R2[i]>0.6 and bang:
        bang = False
        plt.plot(cN_time2[i], z2[i], c='r', marker='x', markersize='14')
    if F_neg_R2[i]>0.6 and not bang:
        bang = True
        plt.plot(cN_time2[i], z2[i], c='r', marker='.', markersize='12')
plt.grid()
plt.legend(fontsize=15) 

plt.figure(3)
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=cN_time2[-1]+1, step=0.4), fontsize=18)
plt.ylabel('vertical height (m)', fontsize=22)
plt.xlabel('time (s)', fontsize=22)
plt.plot(cN_time3, z3, linewidth=1.5, label='0.30 m/s')
boom = True
bang = False
for i in range(0, len(F_pos_L3)):
    if F_pos_L3[i]>0.6 and boom:
        boom = False
        plt.plot(cN_time3[i], z3[i], c='k', marker='+', markersize='14')
    if F_neg_L3[i]>0.5 and not boom:
        boom = True
        plt.plot(cN_time3[i], z3[i], c='k', marker='.', markersize='12')
    if F_pos_R3[i]>0.6 and bang:
        bang = False
        plt.plot(cN_time3[i], z3[i], c='r', marker='x', markersize='14')
    if F_neg_R3[i]>0.6 and not bang:
        bang = True
        plt.plot(cN_time3[i], z3[i], c='r', marker='.', markersize='12')
plt.grid()
plt.legend(fontsize=15) 

plt.show()

# yeet = False
# teet = False
# for i in range(0, len(grf_L1)):
#     if grf_L1[i]>1 and yeet:
#         yeet = False
#         print('l1', cN_time1[i], l1[i]*180/np.pi, 'grounded')
#     if grf_L1[i]<=1 and not yeet:
#         yeet = True
#         print('l1', cN_time1[i], l1[i]*180/np.pi, 'air')
#     if grf_R1[i]>1 and teet:
#         teet = False
#         print('r1', cN_time1[i], r1[i]*180/np.pi, 'grounded')
#     if grf_R1[i]<=1 and not teet:
#         teet = True
#         print('r1', cN_time1[i], r1[i]*180/np.pi, 'air')

# yeet = False
# teet = False
# for i in range(0, len(grf_L2)):
#     if grf_L2[i]>1 and yeet:
#         yeet = False
#         print('l2', cN_time2[i], l2[i]*180/np.pi, 'grounded')
#     if grf_L2[i]<=1 and not yeet:
#         yeet = True
#         print('l2', cN_time2[i], l2[i]*180/np.pi, 'air')
#     if grf_R2[i]>1 and teet:
#         teet = False
#         print('r2', cN_time2[i], r2[i]*180/np.pi, 'grounded')
#     if grf_R2[i]<=1 and not teet:
#         teet = True
#         print('r2', cN_time2[i], r2[i]*180/np.pi, 'air')

# yeet = False
# teet = False
# for i in range(0, len(grf_L3)):
#     if grf_L3[i]>1 and yeet:
#         yeet = False
#         print('l3', cN_time3[i], l3[i]*180/np.pi, 'grounded')
#     if grf_L3[i]<=1 and not yeet:
#         yeet = True
#         print('l3', cN_time3[i], l3[i]*180/np.pi, 'air')
#     if grf_R3[i]>1 and teet:
#         teet = False
#         print('r3', cN_time3[i], r3[i]*180/np.pi, 'grounded')
#     if grf_R3[i]<=1 and not teet:
#         teet = True
#         print('r3', cN_time3[i], r3[i]*180/np.pi, 'air')

avg = 0
for n in range(0, len(vel_x1)):
    avg += vel_x1[n]
print(avg/len(vel_x1), cN_time1[-1], x1[-1])
avg = 0
for n in range(0, len(vel_x2)):
    avg += vel_x2[n]
print(avg/len(vel_x2), cN_time2[-1])
avg = 0
for n in range(0, len(vel_x3)):
    avg += vel_x3[n]
print(avg/len(vel_x3), cN_time3[-1])
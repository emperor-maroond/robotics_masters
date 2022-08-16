import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cloudpickle
from scipy.interpolate import interp1d

m1 = [] # 0.7 m/s SS
with open("Optimisation_Code/Feasible_Solution/02/steady-state.pkl", "rb") as f:
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
with open("Optimisation_Code/Feasible_Solution/03/steady-state.pkl", "rb") as f:
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
t = []
adder = 0
for i in range(0, len(m2)):
    if(i>0):
        adder += m2[i-1].q[N2,cN2,'x'].value
    for n in range(1, N2+1):
        for c in range(1, cN2+1):
            z2.append(m2[i].q[n,c,'z'].value)
            vel_z2.append(m2[i].dq[n,c,'z'].value)
            t.append(m2[i].tt0[n].value - m1[i].tt0[1].value)
            x2.append(m2[i].q[n,c,'x'].value + adder) 
            vel_x2.append(m2[i].dq[n,c,'x'].value)
            r2.append(m2[i].q[n,c,'theta_l_R'].value*180/np.pi)
            l2.append(m2[i].q[n,c,'theta_l_L'].value*180/np.pi)

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

# The graphs__________________________________________________________________________________________________
z1 = interp1d(cN_time1, z1, kind='slinear')     
xnew1 = np.linspace(0, cN_time1[-1], num=10000, endpoint=True)
z2 = interp1d(cN_time2, z2, kind='slinear')     
xnew2 = np.linspace(0, cN_time2[-1], num=10000, endpoint=True)
z3 = interp1d(cN_time3, z3, kind='slinear')     
xnew3 = np.linspace(0, cN_time3[-1], num=10000, endpoint=True)

plt.figure(1)
plt.xticks(np.arange(start=0, stop=cN_time3[-1]+1, step=0.1))
plt.ylabel('vertical displacement (m)')
plt.xlabel('time (s)')
plt.plot(xnew1, z1(xnew1), linewidth=1, label='0.7 m/s')
plt.plot(xnew2, z2(xnew2), linewidth=1, label='0.5 m/s')
plt.plot(xnew3, z3(xnew3), linewidth=1, label='1.0 m/s')
plt.legend()

vel_z1 = interp1d(cN_time1, vel_z1, kind='slinear')     
vel_z2 = interp1d(cN_time2, vel_z2, kind='slinear')     
vel_z3 = interp1d(cN_time3, vel_z3, kind='slinear')     

plt.figure(2)
plt.xticks(np.arange(start=0, stop=cN_time3[-1]+1, step=0.1))
plt.ylabel('vertical velocity (m/s)')
plt.xlabel('time (s)')
plt.plot(xnew1, vel_z1(xnew1), linewidth=1, label='0.7 m/s')
plt.plot(xnew2, vel_z2(xnew2), linewidth=1, label='0.5 m/s')
plt.plot(xnew3, vel_z3(xnew3), linewidth=1, label='1.0 m/s')
plt.legend()

x1 = interp1d(cN_time1, x1, kind='slinear')     
x2 = interp1d(cN_time2, x2, kind='slinear')     
x3 = interp1d(cN_time3, x3, kind='slinear') 

plt.figure(3)
plt.xticks(np.arange(start=0, stop=cN_time3[-1]+1, step=0.1))
plt.ylabel('horisontal displacement (m)')
plt.xlabel('time (s)')
plt.plot(xnew1, x1(xnew1), linewidth=1, label='0.7 m/s')
plt.plot(xnew2, x2(xnew2), linewidth=1, label='0.5 m/s')
plt.plot(xnew3, x3(xnew3), linewidth=1, label='1.0 m/s')
plt.legend()

vel_x1 = interp1d(cN_time1, vel_x1, kind='slinear')     
vel_x2 = interp1d(cN_time2, vel_x2, kind='slinear')     
vel_x3 = interp1d(cN_time3, vel_x3, kind='slinear')   

plt.figure(4)
plt.xticks(np.arange(start=0, stop=cN_time3[-1]+1, step=0.1))
plt.ylabel('horisontal velocity (m/s)')
plt.xlabel('time (s)')
plt.plot(xnew1, vel_x1(xnew1), linewidth=1, label='0.7 m/s')
plt.plot(xnew2, vel_x2(xnew2), linewidth=1, label='0.5 m/s')
plt.plot(xnew3, vel_x3(xnew3), linewidth=1, label='1.0 m/s')
plt.legend()

plt.show()
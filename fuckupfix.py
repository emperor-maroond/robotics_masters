import cloudpickle
import numpy as np

m1 = [] # 0.7 m/s SS
with open("Optimisation_Code/Feasible_Solution/00/accel.pkl", "rb") as f:
    m1.append(cloudpickle.load(f))    

m2 = [] # 0.5 m/s SS
with open("Optimisation_Code/Feasible_Solution/00/steady-state.pkl", "rb") as f:
    m2.append(cloudpickle.load(f))    

m3 = [] # 1.0 m/s SS
with open("Optimisation_Code/Feasible_Solution/00/decel.pkl", "rb") as f:
    m3.append(cloudpickle.load(f))   

N1 = m1[0].N[-1]
cN1 = m1[0].cN[-1]

N2 = m2[0].N[-1]
cN2 = m2[0].cN[-1]

N3 = m3[0].N[-1]
cN3 = m3[0].cN[-1]

N_time1 = []
cN_time1 = []
cN_adder1 = 0
adder1 = 0
x1 = []
z1 = []
r1 = []
l1 = []
vel_z1 = []
vel_x1 = []
grf_L1 = []
grf_R1 = []
adder = 0


for n in range(1, N1+1):
    N_time1.append(m1[0].tt0[n].value - m1[0].tt0[1].value + adder1)
    for c in range(1, cN1+1):
        cN_time1.append(m1[0].tt[n,c].value - m1[0].tt[1,1].value + cN_adder1)        

for n in range(1, N1+1):
    for c in range(1, cN1+1):
        z1.append(m1[0].q[n,c,'z'].value)
        vel_z1.append(m1[0].dq[n,c,'z'].value)
        vel_x1.append(m1[0].dq[n,c,'x'].value)
        x1.append(m1[0].q[n,c,'x'].value + adder) 
        r1.append(m1[0].q[n,c,'theta_l_R'].value*180/np.pi)
        l1.append(m1[0].q[n,c,'theta_l_L'].value*180/np.pi)
        grf_L1.append(m1[0].GRF_L[n,c,'Z','ps'].value)
        grf_R1.append(m1[0].GRF_R[n,c,'Z','ps'].value)

adder1 += (m1[0].tt0[N1].value - m1[0].tt0[1].value)
cN_adder1 += m1[0].tt0[N1].value - m1[0].tt0[1].value
adder += m1[0].q[N1,cN1,'x'].value
for n in range(1, N2+1):
    for c in range(1, cN2+1):
        N_time1.append(m2[0].tt0[n].value - m2[0].tt0[1].value + adder1)
        cN_time1.append(m2[0].tt[n,c].value - m2[0].tt[1,1].value + cN_adder1)
        z1.append(m2[0].q[n,c,'z'].value)
        vel_z1.append(m2[0].dq[n,c,'z'].value)
        x1.append(m2[0].q[n,c,'x'].value + adder) 
        vel_x1.append(m2[0].dq[n,c,'x'].value)
        r1.append(m2[0].q[n,c,'theta_l_R'].value*180/np.pi)
        l1.append(m2[0].q[n,c,'theta_l_L'].value*180/np.pi)
        grf_L1.append(m2[0].GRF_L[n,c,'Z','ps'].value)
        grf_R1.append(m2[0].GRF_R[n,c,'Z','ps'].value)
        
adder1 += (m2[0].tt0[N2].value - m2[0].tt0[1].value)
cN_adder1 += m2[0].tt0[N2].value - m2[0].tt0[1].value
adder += m2[0].q[N2,cN2,'x'].value
for n in range(1, N3+1):
    for c in range(1, cN3+1):
        N_time1.append(m3[0].tt0[n].value - m3[0].tt0[1].value + adder1)
        cN_time1.append(m3[0].tt[n,c].value - m3[0].tt[1,1].value + cN_adder1)
        z1.append(m3[0].q[n,c,'z'].value)
        vel_z1.append(m3[0].dq[n,c,'z'].value)
        x1.append(m3[0].q[n,c,'x'].value + adder) 
        vel_x1.append(m3[0].dq[n,c,'x'].value)
        r1.append(m3[0].q[n,c,'theta_l_R'].value*180/np.pi)
        l1.append(m3[0].q[n,c,'theta_l_L'].value*180/np.pi)
        grf_L1.append(m3[0].GRF_L[n,c,'Z','ps'].value)
        grf_R1.append(m3[0].GRF_R[n,c,'Z','ps'].value)



file = open('traj.csv', 'w')
file.write('{}\n'.format(list(cN_time1)))
file.write('{}\n'.format(list(x1)))
file.write('{}\n'.format(list(z1)))
file.write('{}\n'.format(list(vel_x1)))
file.write('{}\n'.format(list(vel_z1)))
file.close()
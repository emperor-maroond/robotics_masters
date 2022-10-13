import cloudpickle
import numpy as np
import matplotlib.pyplot as plt

# plt.style.use(['fivethirtyeight','seaborn-deep'])
# %matplotlib inline

# Insert all the data_________________________________________________________________________________________________________
m1 = []
with open("Optimisation_Code/Feasible_Solution/damp_x2/steady-state.pkl", "rb") as f:
    m1.append(cloudpickle.load(f)) 

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
rr = []
lr = []
l = m1[0].ll1
vel_r = []
vel_l = []
adder = 0

N1 = m1[0].N[-1]
cN1 = m1[0].cN[-1]

for n in range(1, N1+1):
    N_time1.append(m1[0].tt0[n].value - m1[0].tt0[1].value + adder1)
    for c in range(1, cN1+1):
        cN_time1.append((m1[0].tt[n,c].value - m1[0].tt[1,1].value + cN_adder1) * 1.3)        

for n in range(1, N1+1):
    for c in range(1, cN1+1):
        z1.append(m1[0].q[n,c,'z'].value)
        vel_z1.append(m1[0].dq[n,c,'z'].value)
        vel_x1.append(m1[0].dq[n,c,'x'].value * (100-48.738)/100)
        x1.append(m1[0].q[n,c,'x'].value + adder) 
        r1.append(m1[0].q[n,c,'theta_l_R'].value)
        l1.append(m1[0].q[n,c,'theta_l_L'].value)
        grf_L1.append(m1[0].GRF_L[n,c,'Z','ps'].value)
        grf_R1.append(m1[0].GRF_R[n,c,'Z','ps'].value)
        lr.append(m1[0].q[n, c,'r_L'].value)
        rr.append(m1[0].q[n, c,'r_R'].value)
        vel_r.append(m1[0].dq[n,c,'theta_l_R'].value)
        vel_l.append(m1[0].dq[n,c,'theta_l_L'].value)

Ts = 250/1000

plt.plot(cN_time1, z1)
# plt.plot(cN_time1, grf_L1)

Ts = []
vel1 = []
vel2 = []

yeet = True
teet = True
for i in range(0, len(grf_L1)):
    if grf_L1[i]>0.01 and yeet:
        yeet = False
        print('l1', cN_time1[i], (l+lr[i])*np.cos(l1[i]), 'grounded')
        tmp = cN_time1[i]
        vel1.append(vel_x1[i])
    if grf_L1[i]<=0.01 and not yeet:
        yeet = True
        print('l1', cN_time1[i], (l+lr[i])*np.cos(l1[i]), 'air')
        Ts.append(cN_time1[i]-tmp)
        vel2.append(vel_x1[i])
    if grf_R1[i]>0.01 and teet:
        teet = False
        print('r1', cN_time1[i], (l+rr[i])*np.cos(r1[i]), 'grounded')
        tmp = cN_time1[i]
        vel1.append(vel_x1[i])
    if grf_R1[i]<=0.01 and not teet:
        teet = True
        print('r1', cN_time1[i], (l+rr[i])*np.cos(r1[i]), 'air')
        Ts.append(cN_time1[i]-tmp)
        vel2.append(vel_x1[i])

for i in range(len(Ts)):
    xf = (Ts[i]*vel1[i])/2
    print(xf, (Ts[i]*vel2[i])/2)

plt.show()
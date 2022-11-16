from audioop import avg
import cloudpickle
import numpy as np

m1 = [] # 0.7 m/s SS
with open("Optimisation_Code/Feasible_Solution/damp_x2/accel.pkl", "rb") as f:
    m1.append(cloudpickle.load(f))    

m2 = [] # 0.5 m/s SS
with open("Optimisation_Code/Feasible_Solution/damp_x2/steady-state.pkl", "rb") as f:
    m2.append(cloudpickle.load(f))    

m3 = [] # 1.0 m/s SS
with open("Optimisation_Code/Feasible_Solution/damp_x2/decel.pkl", "rb") as f:
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
b1 = []
vel_z1 = []
vel_x1 = []
grf_L1 = []
grf_R1 = []
adder = 0

def shorten(arr, low, high, t):
    tmp = []
    for i in range(0, len(arr)):
        if t[i] > low and t[i] < high:
            tmp.append(arr[i])
    return tmp

for n in range(1, N1+1):
    N_time1.append(m1[0].tt0[n].value - m1[0].tt0[1].value + adder1)
    for c in range(1, cN1+1):
        cN_time1.append((m1[0].tt[n,c].value - m1[0].tt[1,1].value + cN_adder1) * (100+0)/100)        

for n in range(1, N1+1):
    for c in range(1, cN1+1):
        z1.append(m1[0].q[n,c,'z'].value)
        vel_z1.append(m1[0].dq[n,c,'z'].value)
        vel_x1.append(m1[0].dq[n,c,'x'].value * (100-0)/100)
        x1.append(m1[0].q[n,c,'x'].value + adder) 
        r1.append(m1[0].q[n,c,'theta_l_R'].value*180/np.pi)
        l1.append(m1[0].q[n,c,'theta_l_L'].value*180/np.pi)
        grf_L1.append(m1[0].GRF_L[n,c,'Z','ps'].value)
        grf_R1.append(m1[0].GRF_R[n,c,'Z','ps'].value)
        b1.append(m1[0].q[n,c,'theta_b'].value*180/np.pi)

N_time2 = []; x2 = []; z2 = []; r2 = []; l2 = []; vel_z2 = []; vel_x2 = []; cN_time2 = []; b2 = []
for n in range(1, N2+1):
    for c in range(1, cN2+1):
        N_time2.append(m2[0].tt0[n].value - m2[0].tt0[1].value)
        cN_time2.append((m2[0].tt[n,c].value - m2[0].tt[1,1].value)*1.3)
        z2.append(m2[0].q[n,c,'z'].value)
        vel_z2.append(m2[0].dq[n,c,'z'].value)
        x2.append(m2[0].q[n,c,'x'].value) 
        vel_x2.append(m2[0].dq[n,c,'x'].value * (100-48.738)/100)
        r2.append(m2[0].q[n,c,'theta_l_R'].value*180/np.pi)
        l2.append(m2[0].q[n,c,'theta_l_L'].value*180/np.pi)
        b2.append(m1[0].q[n,c,'theta_b'].value*180/np.pi)

z2 = shorten(z2, 1.39, 2.8, cN_time2)
vel_z2 = shorten(vel_z2, 1.39, 2.8, cN_time2)
x2 = shorten(x2, 1.39, 2.8, cN_time2) 
vel_x2 = shorten(vel_x2, 1.39, 2.8, cN_time2)
r2 = shorten(r2, 1.39, 2.8, cN_time2)
l2 = shorten(l2, 1.39, 2.8, cN_time2)
b2 = shorten(b2, 1.39, 2.8, cN_time2)
cN_time2 = shorten(cN_time2, 1.39, 2.8, cN_time2)
a = cN_time2[0]
cN_time2 = [(x-a) for x in cN_time2]
a = x2[0]
x2 = [(x-a) for x in x2]
for i in range(len(cN_time2)):
    if cN_time2[i] < 0.3:
        z2[i] = z2[i] * 0.95


adder1 += (m1[0].tt0[N1].value - m1[0].tt0[1].value)
cN_adder1 += (m1[0].tt0[N1].value - m1[0].tt0[1].value) * (100+0)/100
adder += m1[0].q[N1,cN1,'x'].value
for i in range(len(cN_time2)):
    N_time1.append(N_time2[i] + adder1)
    cN_time1.append(cN_time2[i] + cN_adder1)
    z1.append(z2[i])
    vel_z1.append(vel_z2[i])
    x1.append(x2[i] + adder) 
    vel_x1.append(vel_x2[i])
    r1.append(r2[i])
    l1.append(l2[i])
    b1.append(b2[i])

adder1 += (N_time2[-1])
cN_adder1 += cN_time2[-1]
adder += x2[-1]
for i in range(len(cN_time2)):
    N_time1.append(N_time2[i] + adder1)
    cN_time1.append(cN_time2[i] + cN_adder1)
    z1.append(z2[i])
    vel_z1.append(vel_z2[i])
    x1.append(x2[i] + adder) 
    vel_x1.append(vel_x2[i])
    r1.append(r2[i])
    l1.append(l2[i])
    b1.append(b2[i])

# adder1 += (m2[0].tt0[N2].value - m2[0].tt0[1].value)
# cN_adder1 += (m2[0].tt0[N2].value - m2[0].tt0[1].value) * 1.3
# adder += m2[0].q[N2,cN2,'x'].value\
adder1 += (N_time2[-1])
cN_adder1 += cN_time2[-1]
adder += x2[-1]
for n in range(1, N3+1):
    for c in range(1, cN3+1):
        N_time1.append(m3[0].tt0[n].value - m3[0].tt0[1].value + adder1)
        cN_time1.append((m3[0].tt[n,c].value - m3[0].tt[1,1].value)*(100+0)/100 + cN_adder1)
        z1.append(m3[0].q[n,c,'z'].value)
        vel_z1.append(m3[0].dq[n,c,'z'].value)
        x1.append(m3[0].q[n,c,'x'].value + adder) 
        vel_x1.append(m3[0].dq[n,c,'x'].value * (100-0)/100)
        r1.append(m3[0].q[n,c,'theta_l_R'].value*180/np.pi)
        l1.append(m3[0].q[n,c,'theta_l_L'].value*180/np.pi)
        grf_L1.append(m3[0].GRF_L[n,c,'Z','ps'].value)
        grf_R1.append(m3[0].GRF_R[n,c,'Z','ps'].value)
        b1.append(m1[0].q[n,c,'theta_b'].value*180/np.pi)



file = open('traj.csv', 'w')
file.write('{}\n'.format(list(cN_time1)))
file.write('{}\n'.format(list(x1)))
file.write('{}\n'.format(list(z1)))
file.write('{}\n'.format(list(vel_x1)))
file.write('{}\n'.format(list(vel_z1)))
file.write('{}\n'.format(list(grf_L1)))
file.write('{}\n'.format(list(grf_R1)))
file.write('{}\n'.format(list(r1)))
file.write('{}\n'.format(list(l1)))
file.write('{}\n'.format(list(b1)))
file.close()

# avg = 0
# for i in vel_z1:
#     avg += i
# print(avg/len(vel_z1))
import csv
import numpy as np
import matplotlib.pyplot as plt
from re import sub

# plt.style.use(['fivethirtyeight','seaborn-deep'])
# %matplotlib inline

# Insert all the data_________________________________________________________________________________________________________

def make_list(data):
    ans = []
    for i in range(0, len(data)):
        tmp = float(sub('[\([{})\]]', '', (data[i])))
        ans.append(tmp)
        # print(ans)
    return ans

file = open('traj.csv')
csvreader = csv.reader(file)
rows = []
for row in csvreader:
        rows.append(row)
file.close()
cN_time1 = make_list(rows[0])
x1 = make_list(rows[1])
z1 = make_list(rows[2])
vel_x1 = make_list(rows[3])
vel_z1 = make_list(rows[4])
grf_L1 = make_list(rows[5])
grf_R1 = make_list(rows[6])

# file = open('droid/src/bot_description/scripts/data/0.65data.csv')
file = open('droid/src/bot_description/scripts/data/sim.csv')
csvreader = csv.reader(file)
rows = []
for row in csvreader:
        rows.append(row)
file.close()

sim_r_ser = make_list(rows[1])
sim_l_ser = make_list(rows[3])
sim_height = make_list(rows[5])
sim_dist = make_list(rows[7])
# sim_angle = make_list(rows[9])
sim_time = make_list(rows[11])

value = sim_dist[0]
for i in range(0, len(sim_dist)):
    sim_dist[i] = -sim_dist[i] + value

value = sim_time[0]
for i in range(0, len(sim_time)):
    sim_time[i] = sim_time[i] - value

sim_height = [(x+0.22) for x in sim_height]

# file = open('droid/src/bot_description/scripts/data/freebod.csv')
file = open('droid/src/bot_description/scripts/data/main_data_v2.csv')
csvreader = csv.reader(file)
rows = []
for row in csvreader:
        rows.append(row)
file.close()

r_ser = make_list(rows[97])
l_ser = make_list(rows[99])
enc1 = make_list(rows[101])
enc2 = make_list(rows[103])
enc3 = []

# r_ser = make_list(rows[1])
# l_ser = make_list(rows[3])
# enc1 = make_list(rows[5])
# enc2 = make_list(rows[7])
# enc3 = make_list(rows[9])

# file = open('droid/src/bot_description/scripts/data/free_rough.csv')
file = open('droid/src/bot_description/scripts/data/rough_data.csv')
csvreader = csv.reader(file)
rows = []
for row in csvreader:
        rows.append(row)
file.close()

rr_ser = make_list(rows[1])
rl_ser = make_list(rows[3])
renc1 = make_list(rows[5])
renc2 = make_list(rows[7])
renc3 = []
# renc3 = make_list(rows[9])
    
# Handel the sensor data_____________________________________________________________________________________________________________
def kalman(u):
    p = 500
    r = 40 #50
    h = 1
    q = 0.7 #0.6
    k = 0
    new = [0] * len(u)
    u_hat = 0
    for i in range(0,len(u)):
        k = p*h/(h*p*h+r)
        u_hat = u_hat+k*(u[i] - h*u_hat)
        new[i] = u_hat
        p = (1-k*h)*p+q
    return new

for i in range(0, len(enc1)):
    enc1[i] = 0.84*np.sin(enc1[i]*np.pi/180.0)

for i in range(0, len(renc1)):
    renc1[i] = 0.84*np.sin(renc1[i]*np.pi/180.0)    

for i in range(0, len(enc3)):
    enc3[i] = (90 - enc3[i])*np.pi/180.0

for i in range(0, len(renc3)):
    renc3[i] = (90 - renc3[i])*np.pi/180.0
    
for i in range(0, len(r_ser)):
    r_ser[i] = r_ser[i]*np.pi/180.0
    l_ser[i] = l_ser[i]*np.pi/180.0

# Plot the data______________________________________________________________________________________________________________________
dt = 10/1000
t = np.arange(start=0, stop=len(enc1)*dt, step=dt)
rt = np.arange(start=0, stop=len(renc1)*dt, step=dt)
# l = np.arange(0, len(kal_rough)*dt, dt)

def velocity(pos, t):
    vel = []
    for i in range(0, len(pos)-1):
        tmp = (pos[i+1]-pos[i])/(t[i+1]-t[i])
        vel.append(tmp)
    vel.append(0)
    return vel  

def shorten(arr, low, high, t):
    tmp = []
    for i in range(0, len(arr)):
        if t[i] > low and t[i] < high:
            tmp.append(arr[i])
    return tmp

kal_r = kalman(r_ser)
kal_l = kalman(l_ser)
kal_z = kalman(enc1)
kal_x = kalman(enc2)
kal_theta = kalman(enc3)
rkal_r = kalman(rr_ser)
rkal_l = kalman(rl_ser)
rkal_z = kalman(renc1)
rkal_x = kalman(renc2)
rkal_theta = kalman(renc3)
sim_dist = kalman(sim_dist)
sim_height = kalman(sim_height)

a = 3.0; b = 7.5; c = 7.33; d = c+(b-a)
o = 0.0; p = 5 #o+(b-a)
# a = 5.35; b = 10.1; c = 3.05; d = c+(b-a)
# o = 0.0; p = 5 #o+(b-a)
kal_r = shorten(kal_r, a, b, t)
kal_l = shorten(kal_l, a, b, t)
kal_z = shorten(kal_z, a, b, t)
kal_x = shorten(kal_x, a, b, t)
kal_theta = shorten(kal_theta, a, b, t)
rkal_r = shorten(rkal_r, c, d, rt)
rkal_l = shorten(rkal_l, c, d, rt)
rkal_z = shorten(rkal_z, c, d, rt)
rkal_x = shorten(rkal_x, c, d, rt)
rkal_theta = shorten(rkal_theta, c, d, rt)
sim_dist = shorten(sim_dist, o, p, sim_time)
sim_height = shorten(sim_height, o, p, sim_time)
sim_time = shorten(sim_time, o, p, sim_time)

t = np.arange(start=0, stop=len(kal_z)*dt, step=dt)
rt = np.arange(start=0, stop=len(rkal_z)*dt, step=dt)
value = sim_time[0]

vel_x = velocity(kal_x, t)
vel_z = velocity(kal_z, t)
vel_r = velocity(kal_r, t)
vel_l = velocity(kal_l, t)
rvel_x = velocity(rkal_x, rt)
rvel_z = velocity(rkal_z, rt)
rvel_r = velocity(rkal_r, rt)
rvel_l = velocity(rkal_l, rt)
sim_vel_x = velocity(sim_dist, sim_time)
sim_vel_z = velocity(sim_height, sim_time)

# sim_time = [(x-value) for x in sim_time]

# plt.figure(1)
# plt.yticks(fontsize=18)
# plt.xticks(np.arange(start=0, stop=len(kal_z)*dt, step=0.5), fontsize=18)
# # plt.xticks(np.arange(start=0, stop=p, step=0.5), fontsize=18)
# plt.ylabel('horizontal distance (m)', fontsize=22)
# plt.xlabel('time(s)', fontsize=22)
# plt.grid()
# plt.plot(cN_time1, x1, linewidth=1.5, label='optimiser')
# # plt.plot(t, kal_x, linewidth=1.5, label='rigid surface')
# plt.plot(rt, rkal_x, linewidth=1.5, label='rough surface')
# # plt.plot(sim_time, sim_di
# # st, linewidth=1.5, label='simulation')
# plt.legend(fontsize=18)
# plt.tight_layout()

plt.figure(2)
# plt.ylim([0, 0.7])
plt.yticks(fontsize=18)
plt.xticks(np.arange(start=0, stop=p, step=0.5), fontsize=18)
plt.ylabel('vertical height (m)', fontsize=22)
plt.xlabel('time(s)', fontsize=22)
plt.grid()
plt.plot(cN_time1, z1, linewidth=1.5, label='optimiser')
# plt.plot(t, kal_z, linewidth=1.5, label='rigid surface')
# plt.plot(rt, rkal_z, linewidth=1.5, label='rough surface')
# plt.plot(sim_time, sim_height, linewidth=1.5, label='simulation')
plt.legend(fontsize=18)
plt.tight_layout()

# plt.figure(3)
# # plt.ylim([-0.2, 0.8])
# plt.yticks(fontsize=18)
# plt.xticks(np.arange(start=0, stop=p, step=0.5), fontsize=18)
# plt.ylabel('horizontal velocity (m/s)', fontsize=22)
# plt.xlabel('time(s)', fontsize=22)
# plt.grid()
# plt.plot(cN_time1, vel_x1, linewidth=1.5, label='optimiser')
# # plt.plot(t, vel_x, linewidth=1.5, label='rigid surface')
# plt.plot(rt, rvel_x, linewidth=1.5, label='rough surface')
# # plt.plot(sim_time, sim_vel_x, linewidth=1.5, label='simulation')
# plt.legend(fontsize=18)
# plt.tight_layout()

# plt.figure(4)
# # plt.ylim([-1.8, 2.9])
# plt.yticks(fontsize=18)
# plt.xticks(np.arange(start=0, stop=p, step=0.5), fontsize=18)
# plt.ylabel('vertical velocity (m/s)', fontsize=22)
# plt.xlabel('time(s)', fontsize=22)
# plt.grid()
# plt.plot(cN_time1, vel_z1, linewidth=1.5, label='optimiser')
# # plt.plot(t, vel_z, linewidth=1.5, label='rigid surface')
# plt.plot(rt, rvel_z, linewidth=1.5, label='rough surface')
# # plt.plot(sim_time, sim_vel_z, linewidth=1.5, label='simulation')
# plt.legend(fontsize=18)
# plt.tight_layout()

# plt.figure(5)
# plt.yticks(fontsize=18)
# plt.xticks(np.arange(start=0, stop=len(kal_z)*dt, step=0.5), fontsize=18)
# plt.ylabel('body angle (rad)', fontsize=22)
# plt.xlabel('time(s)', fontsize=22)
# plt.grid()
# plt.plot(t, kal_theta, linewidth=1.5, label='normal')
# plt.plot(rt, rkal_theta, linewidth=1.5, label='rough surface')
# plt.legend(fontsize=15)

# grouned_z = []
# grouned_x = []
# grouned_velz = []
# air_z = []
# air_x = []
# air_velz = []
# rgrouned_z = []
# rgrouned_x = []
# rgrouned_velz = []
# rair_z = []
# rair_x = []
# rair_velz = []
# grouned_z1 = []
# grouned_x1 = []
# grouned_velz1 = []
# air_z1 = []
# air_x1 = []
# air_velz1 = []
# fig = plt.figure()
# ax = fig.gca(projection ='3d')
# # plt.title('Vertical Position vs Velocity')
# # plt.yticks(fontsize=18)
# # plt.xticks(fontsize=18)
# ax.set_xlabel('vertical velocity (m/s)')
# ax.set_zlabel('vertical height (m)')
# ax.set_ylabel('horizontal distance (m)')

# height = 0.1
# height = 0.25
# for i in range(0, len(kal_z)):
#     if kal_z[i] <= height:
#         grouned_z.append(kal_z[i])
#         grouned_x.append(kal_x[i])
#         grouned_velz.append(vel_z[i])
#         air_z.append(np.nan)
#         air_x.append(np.nan)
#         air_velz.append(np.nan) 
#     if rkal_z[i] <= height:
#         rgrouned_z.append(rkal_z[i])
#         rgrouned_x.append(rkal_x[i])
#         rgrouned_velz.append(rvel_z[i])
#         rair_z.append(np.nan)
#         rair_x.append(np.nan)
#         rair_velz.append(np.nan) 
#     if kal_z[i] > height:
#         air_z.append(kal_z[i])
#         air_x.append(kal_x[i])
#         air_velz.append(vel_z[i])
#         grouned_z.append(np.nan)
#         grouned_x.append(np.nan)
#         grouned_velz.append(np.nan) 
#     if rkal_z[i] > height:
#         rair_z.append(rkal_z[i])
#         rair_x.append(rkal_x[i])
#         rair_velz.append(rvel_z[i])
#         rgrouned_z.append(np.nan)
#         rgrouned_x.append(np.nan)
#         rgrouned_velz.append(np.nan) 

# ax.plot(vel_z, kal_x, kal_z, linewidth=1, c='r')
# ax.plot(grouned_velz, grouned_x, grouned_z, linewidth=1, c='r')        
# ax.plot(air_velz, air_x, air_z, linewidth=1, c='b')
# # ax.plot(rvel_z, rkal_x, rkal_z, linewidth=1, c='r', linestyle='dotted')
# ax.plot(rgrouned_velz, rgrouned_x, rgrouned_z, linewidth=2, c='r', linestyle='dotted')        
# ax.plot(rair_velz, rair_x, rair_z, linewidth=2, c='b', linestyle='dotted')

# height = 0.28
# for i in range(0, len(z1)):
#     if z1[i]<=height:
#         grouned_z1.append(z1[i])
#         grouned_x1.append(x1[i])
#         grouned_velz1.append(vel_z1[i])
#         air_z1.append(np.nan)
#         air_x1.append(np.nan)
#         air_velz1.append(np.nan) 

#     if z1[i]>height:
#         air_z1.append(z1[i])
#         air_x1.append(x1[i])
#         air_velz1.append(vel_z1[i])
#         grouned_z1.append(np.nan)
#         grouned_x1.append(np.nan)
#         grouned_velz1.append(np.nan)

# ax.plot(vel_z1, x1, z1, linewidth=1, c='r')
# ax.plot(grouned_velz1, grouned_x1, grouned_z1, linewidth=1, c='r')        
# ax.plot(air_velz1, air_x1, air_z1, linewidth=1, c='b')

# avg = 0
# j = 0
# rj = 0
# ravg = 0
# for i in range(0, len(vel_x)):
#     if i>len(vel_x)/2:
#         if round(vel_x[i-1], 5) == 0.0 and round(vel_x[i],5) == 0.0 and round(vel_x[i+1],5) == 0.0:
#             break
#     avg += vel_x[i]
#     j += 1

# for i in range(0, len(rvel_x)):
#     if i>len(rvel_x)/2:
#         if round(rvel_x[i-1],5) == 0.0 and round(rvel_x[i],5) == 0.0 and round(rvel_x[i+1],5) == 0.0:
#             break
#     ravg += rvel_x[i]
#     rj += 1

# avg = avg/j
# ravg = ravg/rj
# print(avg, ravg)

# avg = 0
# for i in range(0, len(vel_x1)):
#     avg += vel_x1[i]
# print(avg/len(vel_x1))

def calculate_ss_vel(height, time, vel_z, vel_x):
    tmp = 0
    rising = 1
    tim = []
    avg_z = 0
    avg_x = 0
    div = 0
    j = 0
    for i in range(len(height)-1):
        j += 1
        if round(height[i], 4) == round(height[i+1], 4) == round(height[i+2], 4) and j>10:
            break
        if tmp < height[i] and rising:
            tmp = height[i]
        if tmp > height[i+1] and rising:
            tmp = 0
            tim.append(time[i])
        if height[i+1]-height[i] < 0:
            rising = 0
        elif height[i+1]-height[i] > 0:
            rising = 1
    
    j = 0
    for i in time:
        if i >= tim[0] and i <= tim[-1]:
            avg_z += vel_z[j]
            avg_x += vel_x[j]
            div += 1
        j+=1

    return avg_z/div, avg_x/div

# print(calculate_ss_vel(sim_height, sim_time, sim_vel_z, sim_vel_x))
print(calculate_ss_vel(kal_z, t, vel_z, vel_x))
print(calculate_ss_vel(rkal_z, rt, rvel_z, rvel_x))

plt.show()
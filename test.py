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

Ts = 250/1000

plt.plot(cN_time1, grf_R1)
plt.plot(cN_time1, grf_L1)
plt.show()

if grf_L1 > 1 and grf_R1 > 1:
    

xf = (Ts*vel_x1)/2
print(xf)
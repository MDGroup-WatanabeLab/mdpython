import os
import math
import numpy as np

# input lattice size
while True:
    flag = 0
    size = input("Please input the lattice size [ x, y, z ] : ").split()
    if len(size) == 3:
        for i in range(len(size)):
            if size[i].isdecimal() and int(size[i]) > 0:
                flag = 1
            else:
                flag = 0
                break
    if flag == 1:
        break

# lattice parameter of unit cell
"""
# from sansoken
l_a = 4.921
l_b = 4.921
l_c = 5.4163
"""
l_a = 4.91304
l_b = 4.91304
l_c = 5.40463

# lattice parameter (matrix format)
l_trigonal = np.array([[l_a * float(size[0]), 0, 0], 
                    [-l_b*math.sin(math.pi/6) * float(size[1]), l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# wycoff position of Si
"""
# from sansoken
x_si = 0.4698
y_si = 0.0
z_si = 1/3
# from bilbao
wyckoff_si = [[x_si, 0.0, 1/3], [0.0, x_si, 2/3], [-x_si, -x_si, 0.0]]
"""

# form wyckoff
x = 0.415
y = 0.272
z = 0.120
u = 0.465
wyckoff_si = [[-u, -u, 1/3], [u, 0, 0], [0, u, 2/3]]

for i in range(len(wyckoff_si)):
    for j in range(3):
        if wyckoff_si[i][j] < 0:
            wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

# wycoff position of O
"""
# from sansoken
x_o = 0.4151
y_o = 0.2675
z_o = 0.2139
# from bilbao
wyckoff_o = [[x_o, y_o, z_o], [-y_o, x_o-y_o, z_o+1/3], [-x_o+y_o, -x_o, z_o+2/3], [y_o, x_o, -z_o], [x_o-y_o, -y_o, -z_o+2/3], [-x_o, -x_o+y_o, -z_o+1/3]]
"""

# from wyckoff
wyckoff_o = [[x, y, z], [y-x, -x, z+1/3], [-y, x-y, z+2/3], [x-y, -y, -z], [y, x, 2/3-z], [-x, y-x, 1/3-z]]
for i in range(len(wyckoff_o)):
    for j in range(3):
        if wyckoff_o[i][j] < 0:
            wyckoff_o[i][j] = 1 + wyckoff_o[i][j]

# cubic lattice parameter (matrix format)
l_cubic = np.array([[l_a * float(size[0]), 0, 0], 
                    [0, l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# coordinate of Si and O
position_si = []
position_o = []

for i in range(int(size[0])):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_si)):
                temp = np.zeros(shape=(3, 1))
                temp[0, 0] = (wyckoff_si[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_si[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_si[l][2] + k)/float(size[2]) 
                si = np.dot(l_trigonal.T, temp)
                
                #if si[0, 0] >= 0 and si[0, 0] <= l_cubic[0, 0]:
                position_si.append("{} {} {}".format(si[0, 0], si[1, 0], si[2, 0]))
                    
for i in range(int(size[0])):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_o)):
                temp = np.zeros(shape=(3, 1))
                temp[0, 0] = (wyckoff_o[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_o[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_o[l][2] + k)/float(size[2])
                o = np.dot(l_trigonal.T, temp)
                
                #if o[0, 0] >= 0 and o[0, 0] <= l_cubic[0, 0]:
                position_o.append("{} {} {}".format(o[0, 0], o[1, 0], o[2, 0]))

# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("Alpha-Quartz_SiO2_{}x{}x{}\n".format(size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_trigonal[i][j]))
    f.write("\n")
f.write("Si O\n")
f.write("{} {}\n".format(len(position_si), len(position_o)))
f.write("Cartesian\n")
for i in position_si:
    f.write(i + "\n")
for i in position_o:
    f.write(i + "\n")
f.close()
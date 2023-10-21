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
l_a = 4.9965
l_b = 4.9965
l_c = 5.4543

# lattice parameter (matrix format)
l_hexagonal = np.array([[l_a * float(size[0]), 0, 0], 
                    [-l_b*math.sin(math.pi/6) * float(size[1]), l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# wycoff position of Si, 3c from ??????????
x_si = 1/2
y_si = 0.0
z_si = 0.0
#wyckoff_si = [[1/2, 0.0, 0.0], [0.0, 1/2, 1/3], [1/2, 1/2, 2/3]]
wyckoff_si = [[0.0, 0.0, 0.0], [1/2, 0.0, 2/3], [0.0, 1/2, 1/3]]
for i in range(len(wyckoff_si)):
    for j in range(3):
        if wyckoff_si[i][j] < 0:
            wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

# wycoff position of O, 6j from ??????????
x_o = 0.4169
y_o = 0.20845
z_o = 5/6
#wyckoff_o = [[x_o, 2*x_o, 1/2], [-2*x_o, -x_o, 5/6], [x_o, -x_o, 1/6], [-x_o, -2*x_o, 1/2], [2*x_o, x_o, 5/6], [-x_o, x_o, 1/6]]
wyckoff_o = [[0.296667, 0.086667, 0.833333], [0.086667, 0.296667, 0.166667], [0.716667, 0.3, 0.5], [0.3, 0.716667, 0.5], [0.703333, 0.913333, 0.833333], [0.913333, 0.703333, 0.166667]]
for i in range(len(wyckoff_o)):
    for j in range(3):
        if wyckoff_o[i][j] < 0:
            wyckoff_o[i][j] = 1 + wyckoff_o[i][j]

# cubic lattice parameter (matrix format)　立方体っぽく切り取る（立方晶ではない）
l_cubic = np.array([[l_a * float(size[0]), 0, 0], 
                    [0, l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# coordinate of Si and O
position_si = []
position_o = []

for i in range(int(size[0])*2):   #斜めだから2倍にしておく
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_si)):
                temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                temp[0, 0] = (wyckoff_si[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_si[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_si[l][2] + k)/float(size[2]) 
                si = np.dot(l_hexagonal.T, temp) # 行列計算により絶対座標へ
                
                if si[0, 0] >= 0 and si[0, 0] <= l_cubic[0, 0] and si[0, 0] != l_a*float(size[0]): 
                    position_si.append("{} {} {}".format(si[0, 0], si[1, 0], si[2, 0]))

                # if you use hexagonal
                #position_o.append("{} {} {}".format(si[0, 0], si[1, 0], si[2, 0]))
                    
for i in range(int(size[0])*2):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_o)):
                temp = np.zeros(shape=(3, 1))
                temp[0, 0] = (wyckoff_o[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_o[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_o[l][2] + k)/float(size[2])
                o = np.dot(l_hexagonal.T, temp)
                
                if o[0, 0] >= 0 and o[0, 0] <= l_cubic[0, 0] and o[0, 0] != l_a*float(size[0]):
                    position_o.append("{} {} {}".format(o[0, 0], o[1, 0], o[2, 0]))
                
                # if you use hexagonal
                #position_o.append("{} {} {}".format(o[0, 0], o[1, 0], o[2, 0]))

# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("Beta-Quartz_SiO2_{}x{}x{}\n".format(size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_cubic[i][j]))
    f.write("\n")
# if you use hexagonal :
#for i in range(3):
    #for j in range(3):
        #f.write("{} ".format(l_cubic[i][j]))
    #f.write("\n")

f.write("Si O\n")
f.write("{} {}\n".format(len(position_si), len(position_o)))
f.write("Cartesian\n")
for i in position_si:
    f.write(i + "\n")
for i in position_o:
    f.write(i + "\n")
f.close()
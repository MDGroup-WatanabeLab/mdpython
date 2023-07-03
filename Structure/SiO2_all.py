import os
import math
import numpy as np

while True:
    atomflag = input(
                        "Select SiO2 types : \n"
                        "0 : a-quartz\n"
                        "1 : b-quartz\n"
                        "2 : b-tridymite\n"
                        "3 : a-cristobalite\n"
                        "4 : b-cristobalite\n"
                        "5 : stishovite\n"
                        "Input number : "
                        )
    if atomflag.isdigit:
        atomflag = int(atomflag)
        if atomflag >= 0 and atomflag < 6:    
            break

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

# lattice parameter of unit cell, 産総研
if atomflag == 0: #a-q
    l_a = 4.921
    l_b = 4.921
    l_c = 5.4163
elif atomflag == 1: #b-q
    l_a = 4.9965
    l_b = 4.9965
    l_c = 5.4543
elif atomflag == 2: #b-tridy
    l_a = 5.052
    l_b = 5.052
    l_c = 8.27
elif atomflag == 3: #a-crist
    l_a = 4.96937
    l_b = 4.96937
    l_c = 6.92563
elif atomflag == 4: #b-crist
    l_a = 7.12637
    l_b = 7.12637
    l_c = 7.12637
elif atomflag == 5: #stishovite
    l_a = 4.1773
    l_b = 4.1773
    l_c = 2.6655
elif atomflag == 6: #coesite
    l_a = 7.17
    l_b = 7.17
    l_c = 12.38

# lattice parameter (matrix format)
l_trigonal = np.array([[l_a * float(size[0]), 0, 0], 
                       [-l_b*math.sin(math.pi/6) * float(size[1]), l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                       [0, 0, l_c * float(size[2])]])

l_tetragonal = np.array([[l_a * float(size[0]), 0, 0], 
                         [0, l_b * float(size[1]), 0], 
                         [0, 0, l_c * float(size[2])]])


# wycoff position of Si, 3a https://www.cryst.ehu.es/ , https://staff.aist.go.jp/nomura-k/japanese/itscgallary.htm
if atomflag == 0: #a-q
    x_si = 0.4698
    y_si = 0.0
    z_si = 1/3
    wyckoff_si = [[x_si, 0.0, 1/3], [0.0, x_si, 2/3], [-x_si, -x_si, 0.0]]
    for i in range(len(wyckoff_si)):
        for j in range(3):
            if wyckoff_si[i][j] < 0:
                wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

    # wycoff position of O, 6c 
    x_o = 0.4151
    y_o = 0.2675
    z_o = 0.2139
    wyckoff_o = [[x_o, y_o, z_o], [-y_o, x_o-y_o, z_o+1/3], [-x_o+y_o, -x_o, z_o+2/3], [y_o, x_o, -z_o], [x_o-y_o, -y_o, -z_o+2/3], [-x_o, -x_o+y_o, -z_o+1/3]]
    for i in range(len(wyckoff_o)):
        for j in range(3):
            if wyckoff_o[i][j] < 0:
                wyckoff_o[i][j] = 1 + wyckoff_o[i][j]
elif atomflag == 1: #b-q
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

elif atomflag == 2: #tridy
    # wycoff position of Si, 194 4f
    x_si = 1/3
    y_si = 2/3
    z_si = 0.0620
    wyckoff_si = [[1/3, 2/3, z_si], [2/3, 1/3, z_si+1/2], [2/3, 1/3, -z_si], [1/3, 2/3, -z_si+1/2]]
    for i in range(len(wyckoff_si)):
        for j in range(3):
            if wyckoff_si[i][j] < 0:
                wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

    # wycoff position of O1, 194 2c
    x_o1 = 1/3
    y_o1 = 2/3
    z_o1 = 1/4
    wyckoff_o1 = [[1/3, 2/3, 1/4], [2/3, 1/3, 3/4]]
    for i in range(len(wyckoff_o1)):
        for j in range(3):
            if wyckoff_o1[i][j] < 0:
                wyckoff_o1[i][j] = 1 + wyckoff_o1[i][j]

    # wycoff position of O2, 194 6g
    x_o2 = 1/2
    y_o2 = 0
    z_o2 = 0
    wyckoff_o2 = [[1/2, 0, 0], [0, 1/2, 0], [1/2, 1/2, 0],
                  [1/2, 0, 1/2], [0, 1/2, 1/2], [1/2, 1/2, 1/2]]
    for i in range(len(wyckoff_o2)):
        for j in range(3):
            if wyckoff_o2[i][j] < 0:
                wyckoff_o2[i][j] = 1 + wyckoff_o2[i][j]


elif atomflag == 3: #a-cryst
    # wycoff position of Si, 92 4a
    x_si = 0.3006
    y_si = 0.3006
    z_si = 0.0
    wyckoff_si = [[x_si, x_si, 0.0], [-x_si, -x_si, 1/2], [-x_si+1/2, x_si+1/2, 1/4], [x_si+1/2, -x_si+1/2, 3/4]]
    for i in range(len(wyckoff_si)):
        for j in range(3):
            if wyckoff_si[i][j] < 0:
                wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

    # wycoff position of O, 92 8c 
    x_o = 0.2932
    y_o = 0.1049
    z_o = 0.1789
    wyckoff_o = [[x_o, y_o, z_o], [-x_o, -y_o, z_o+1/2], [-y_o+1/2, x_o+1/2, z_o+1/4], [y_o+1/2, -x_o+1/2, z_o+3/4], [-x_o+1/2, y_o+1/2, -z_o+1/4], [x_o+1/2, -y_o+1/2, -z_o+3/4], [y_o, x_o, -z_o], [-y_o, -x_o, -z_o+1/2]]
    for i in range(len(wyckoff_o)):
        for j in range(3):
            if wyckoff_o[i][j] < 0:
                wyckoff_o[i][j] = 1 + wyckoff_o[i][j]

elif atomflag == 4: #b-cryst
    # wycoff position of Si, 227 8a
    x_si = 0.0
    y_si = 0.0
    z_si = 0.0
    wyckoff_si = [[1/8, 1/8, 1/8], [5/8, 1/8, 5/8],[5/8, 5/8, 1/8],[1/8, 5/8, 5/8],
                  [7/8, 3/8, 3/8], [7/8, 7/8, 7/8],[3/8, 7/8, 3/8],[3/8, 3/8, 7/8]]
    for i in range(len(wyckoff_si)):
        for j in range(3):
            if wyckoff_si[i][j] < 0:
                wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

    # wycoff position of O, 227 16c
    x_o = 1/8
    y_o = 1/8
    z_o = 1/8
    wyckoff_o = [[0, 0, 0], [1/2, 0, 1/2], [0, 1/2, 1/2], [1/2, 1/2, 0],
                 [3/4, 1/4, 1/2],[1/4, 1/4, 0],[3/4, 3/4, 0],[1/4, 3/4, 1/2],
                 [1/4, 1/2, 3/4],[3/4, 1/2, 1/4],[1/4, 0, 1/4],[3/4, 0, 3/4],
                 [1/2, 3/4, 1/4],[0, 3/4, 3/4],[1/2, 1/4, 3/4],[0, 1/4, 1/4],]
    for i in range(len(wyckoff_o)):
        for j in range(3):
            if wyckoff_o[i][j] < 0:
                wyckoff_o[i][j] = 1 + wyckoff_o[i][j]
elif atomflag == 5: #stishovite
    x_si = 0
    y_si = 0
    z_si = 0
    wyckoff_si = [[0, 0, 0], [1/2, 1/2, 1/2]]
    for i in range(len(wyckoff_si)):
        for j in range(3):
            if wyckoff_si[i][j] < 0:
                wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

    # wycoff position of O, 4f 
    x_o = 0.30608
    y_o = 0.30608
    z_o = 0
    wyckoff_o= [[x_o, x_o, 0], [-x_o, -x_o, 0], [-x_o+1/2, x_o+1/2, 1/2], [x_o+1/2, -x_o+1/2, 1/2]]
    for i in range(len(wyckoff_o)):
        for j in range(3):
            if wyckoff_o[i][j] < 0:
                wyckoff_o[i][j] = 1 + wyckoff_o[i][j]

elif atomflag == 6: #coesite
    # wycoff position of Si, 4a
    x_si = 0
    y_si = 0
    z_si = 0
    wyckoff_si = [[0, 0, 0], [0, 1/2, 0], [1/2, 0, 1/2], [1/2, 1/2, 1/2]]
    for i in range(len(wyckoff_si)):
        for j in range(3):
            if wyckoff_si[i][j] < 0:
                wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

    # wycoff position of O1, 4e
    x_o1 = 1/3
    y_o1 = 2/3
    z_o1 = 1/4
    wyckoff_o1 = [[1/3, 2/3, 1/4], [2/3, 1/3, 3/4]]
    for i in range(len(wyckoff_o1)):
        for j in range(3):
            if wyckoff_o1[i][j] < 0:
                wyckoff_o1[i][j] = 1 + wyckoff_o1[i][j]

    # wycoff position of O2, 194 6g
    x_o2 = 1/2
    y_o2 = 0
    z_o2 = 0
    wyckoff_o2 = [[1/2, 0, 0], [0, 1/2, 0], [1/2, 1/2, 0],
                  [1/2, 0, 1/2], [0, 1/2, 1/2], [1/2, 1/2, 1/2]]
    for i in range(len(wyckoff_o2)):
        for j in range(3):
            if wyckoff_o2[i][j] < 0:
                wyckoff_o2[i][j] = 1 + wyckoff_o2[i][j]

# cubic lattice parameter (matrix format)　立方体っぽく切り取る（立方晶ではない）
l_cubic = np.array([[l_a * float(size[0]), 0, 0], 
                    [0, l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# coordinate of Si and O
position_si = []
position_o = []

if atomflag == 0 or atomflag == 1:
    for i in range(int(size[0])*2):   #斜めだから2倍にしておく
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_si)):
                    temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                    temp[0, 0] = (wyckoff_si[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_si[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_si[l][2] + k)/float(size[2]) 
                    si = np.dot(l_trigonal.T, temp) # 行列計算により絶対座標へ
                    
                    if si[0, 0] >= 0 and si[0, 0] <= l_cubic[0, 0]: # 
                        position_si.append("{} {} {}".format(si[0, 0], si[1, 0], si[2, 0]))
                        
    for i in range(int(size[0])*2):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_o)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_o[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_o[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_o[l][2] + k)/float(size[2])
                    o = np.dot(l_trigonal.T, temp)
                    
                    if o[0, 0] >= 0 and o[0, 0] <= l_cubic[0, 0]:
                        position_o.append("{} {} {}".format(o[0, 0], o[1, 0], o[2, 0]))

elif atomflag == 3 or atomflag == 4 or atomflag == 5:
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_si)):
                    temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                    temp[0, 0] = (wyckoff_si[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_si[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_si[l][2] + k)/float(size[2]) 
                    si = np.dot(l_tetragonal.T, temp) # 行列計算により絶対座標へ
                    
                    #if si[0, 0] >= 0 and si[0, 0] <= l_cubic[0, 0]: # 
                    position_si.append("{} {} {}".format(si[0, 0], si[1, 0], si[2, 0]))
                        
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_o)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_o[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_o[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_o[l][2] + k)/float(size[2])
                    o = np.dot(l_tetragonal.T, temp)
                    
                    #if o[0, 0] >= 0 and o[0, 0] <= l_cubic[0, 0]:
                    position_o.append("{} {} {}".format(o[0, 0], o[1, 0], o[2, 0]))
                        
elif atomflag == 2: #b-tridy
    for i in range(int(size[0])*2):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_si)):
                    temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                    temp[0, 0] = (wyckoff_si[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_si[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_si[l][2] + k)/float(size[2]) 
                    si = np.dot(l_trigonal.T, temp) # 行列計算により絶対座標へ
                    
                    if si[0, 0] >= 0 and si[0, 0] <= l_cubic[0, 0]: 
                        position_si.append("{} {} {}".format(si[0, 0], si[1, 0], si[2, 0]))
                        
    for i in range(int(size[0])*2):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_o1)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_o1[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_o1[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_o1[l][2] + k)/float(size[2])
                    o1 = np.dot(l_trigonal.T, temp)
                    
                    if o1[0, 0] >= 0 and o1[0, 0] <= l_cubic[0, 0]:
                        position_o.append("{} {} {}".format(o1[0, 0], o1[1, 0], o1[2, 0]))

    for i in range(int(size[0])*2):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_o2)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_o2[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_o2[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_o2[l][2] + k)/float(size[2])
                    o2 = np.dot(l_trigonal.T, temp)
                    
                    if o2[0, 0] >= 0 and o2[0, 0] <= l_cubic[0, 0]:
                        position_o.append("{} {} {}".format(o2[0, 0], o2[1, 0], o2[2, 0]))

# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")

f.write("Alpha-Quartz_SiO2_{}x{}x{}\n".format(size[0], size[1], size[2]))
f.write("1.0\n")
if atomflag == 0 or atomflag == 1 or atomflag == 2:
    for i in range(3):
        for j in range(3):
            f.write("{} ".format(l_cubic[i][j]))
        f.write("\n")
elif atomflag == 3 or atomflag == 4 or atomflag == 5:
    for i in range(3):
        for j in range(3):
            f.write("{} ".format(l_tetragonal[i][j]))
        f.write("\n")
f.write("Si O\n")
f.write("{} {}\n".format(len(position_si), len(position_o)))
f.write("C\n")
for i in position_si:
    f.write(i + "\n")
for i in position_o:
    f.write(i + "\n")
f.close()
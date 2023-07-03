# Cubic
import os
import math
import numpy as np

atomflag = int(input("Select atoms from following: \n"
                     "0 : Sb \n"
                     "1 : Te \n"
                     "Input number : "))

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

# lattice parameter of unit cell, mp-104
if atomflag == 0: # Sb, wycoff
    l_a = 3.08
    l_b = 3.08
    l_c = 3.08

elif atomflag == 1: # Te, wycoff
    l_a = 3.20
    l_b = 3.20
    l_c = 3.20


# wycoff position 
if atomflag == 0: # Sb, wycoff
    x = 0.0
    y = 0.0
    z = 0.0
    wyckoff = [[0, 0, 0]]
    for i in range(len(wyckoff)):
        for j in range(3):
            if wyckoff[i][j] < 0:
                wyckoff[i][j] = 1 + wyckoff[i][j]

elif atomflag == 1: # Te, wycoff
    x = 0.0
    y = 0.0
    z = 0.0
    wyckoff = [[0, 0, 0]]
    for i in range(len(wyckoff)):
        for j in range(3):
            if wyckoff[i][j] < 0:
                wyckoff[i][j] = 1 + wyckoff[i][j]


l_cubic = np.array([[l_a * float(size[0]), 0, 0], 
                    [0, l_b * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# coordinate 
position = []

for i in range(int(size[0])):   #斜めだから2倍にしておく
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff)):
                temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                temp[0, 0] = (wyckoff[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff[l][2] + k)/float(size[2]) 
                Ap = np.dot(l_cubic.T, temp) # 行列計算により絶対座標へ
                
                if Ap[0, 0] >= 0 and Ap[0, 0] <= l_cubic[0, 0] and Ap[0, 0] != l_a*float(size[0]): # 
                    position.append("{} {} {}".format(Ap[0, 0], Ap[1, 0], Ap[2, 0]))
                    


# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("cubic_{}x{}x{}\n".format(size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_cubic[i][j]))
    f.write("\n")
if atomflag == 0: # Sb
    f.write("Sb\n")
elif atomflag == 1: # Te
    f.write("Te\n")
f.write("{}\n".format(len(position)))
f.write("C\n")
for i in position:
    f.write(i + "\n")

f.close()
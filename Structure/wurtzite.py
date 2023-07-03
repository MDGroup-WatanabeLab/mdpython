# wurtzite structure AB : Hexagonal : ZnS, ZnO, BeO, BN, GaN
import os
import math
import numpy as np

# select Atom
atomflag = int(input("Select atoms from following: \n"
                     "0 : ZnS \n"
                     "1 : ZnO \n"
                     "2 : BeO \n"
                     "3 : BN \n"
                     "4 : GaN \n"
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

# lattice parameter 
if atomflag == 0: # ZnS
    l_a = 3.8227
    l_b = 3.8227
    l_c = 6.2607
elif atomflag == 1: # ZnO
    l_a = 3.24992
    l_b = 3.24992
    l_c = 5.20658
elif atomflag == 2: # BeO
    l_a = 2.6979
    l_b = 2.6979
    l_c = 4.3772
elif atomflag == 3: # BN
    l_a = 2.553
    l_b = 2.553
    l_c = 4.228
elif atomflag == 4: # GaN
    l_a = 3.189
    l_b = 3.189
    l_c = 5.185


# lattice parameter (matrix format)
l_hexagonal = np.array([[l_a * float(size[0]), 0, 0], 
                    [-l_b*math.sin(math.pi/6) * float(size[1]), l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# wycoff position of A
x_A = 1/3
y_A = 2/3
z_A = 0
wyckoff_A = [[1/3, 2/3, z_A], [2/3, 1/3, z_A+1/2]]
for i in range(len(wyckoff_A)):
    for j in range(3):
        if wyckoff_A[i][j] < 0:
            wyckoff_A[i][j] = 1 + wyckoff_A[i][j]

# wycoff position of B
x_B = 1/3
y_B = 2/3
if atomflag == 0: # ZnS
    z_B = 0.3748
elif atomflag == 1: # ZnO
    z_B = 0.3819
elif atomflag == 2: # BeO
    z_B = 0.3786 
elif atomflag == 3: # BN
    z_B = 0.375 
elif atomflag == 4: # GaN ()
    z_B = 0.38  #tentative

wyckoff_B = [[1/3, 2/3, z_B], [2/3, 1/3, z_B+1/2]]
for i in range(len(wyckoff_B)):
    for j in range(3):
        if wyckoff_B[i][j] < 0:
            wyckoff_B[i][j] = 1 + wyckoff_B[i][j]

# cubic lattice parameter (matrix format)　立方体っぽく切り取る（立方晶ではない）
l_cubic = np.array([[l_a * float(size[0]), 0, 0], 
                    [0, l_b * math.cos(math.pi/6) * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# coordinate 
position_A = []
position_B = []

for i in range(int(size[0])*2):  
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_A)):
                temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                temp[0, 0] = (wyckoff_A[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_A[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_A[l][2] + k)/float(size[2]) 
                Ap = np.dot(l_hexagonal.T, temp) # 行列計算により絶対座標へ
                
                if Ap[0, 0] >= 0 and Ap[0, 0] <= l_cubic[0, 0] and Ap[0, 0] != l_a*float(size[0]): # 
                    position_A.append("{} {} {}".format(Ap[0, 0], Ap[1, 0], Ap[2, 0]))
                    
for i in range(int(size[0])*2):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_B)):
                temp = np.zeros(shape=(3, 1))
                temp[0, 0] = (wyckoff_B[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_B[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_B[l][2] + k)/float(size[2])
                Bp = np.dot(l_hexagonal.T, temp)
                
                if Bp[0, 0] >= 0 and Bp[0, 0] <= l_cubic[0, 0] and Bp[0, 0] != l_a*float(size[0]):
                    position_B.append("{} {} {}".format(Bp[0, 0], Bp[1, 0], Bp[2, 0]))

# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("wurtzite_{}x{}x{}\n".format(size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_cubic[i][j]))
    f.write("\n")

if atomflag == 0: # ZnS
    f.write("Zn S\n")
elif atomflag == 1: # ZnO
    f.write("Zn O\n")
elif atomflag == 2: # BeO
    f.write("Be O\n")
elif atomflag == 3: # BN
    f.write("B N\n")
elif atomflag == 4: # GaN
    f.write("Ga N\n")

f.write("{} {}\n".format(len(position_A), len(position_B)))
f.write("Cartesian\n")
for i in position_A:
    f.write(i + "\n")
for i in position_B:
    f.write(i + "\n")
f.close()
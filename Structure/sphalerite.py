# sphalerite structure AB : Hexagonal : ZnS
import os
import math
import numpy as np

# Parameters
atom_name = ["ZnS"]
atom_list = [["Zn", "S"]]
lattice_list = [5.4093]
print("Select atoms from following: ")
for i in range(len(atom_list)):
    print("{} : {}".format(i, atom_name[i]))
atomflag = int(input("Input number : "))


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




# lattice parameter (matrix format)
l_cubic = np.array([[lattice_list[atomflag] * float(size[0]), 0, 0], 
                    [0, lattice_list[atomflag] * float(size[1]), 0], 
                    [0, 0, lattice_list[atomflag] * float(size[2])]])


# wycoff position of A, 4a
x_A = 0
y_A = 0
z_A = 0
wyckoff_A = [[0, 0, 0], [1/2, 1/2, 0], [1/2, 0, 1/2], [0, 1/2, 1/2]]
for i in range(len(wyckoff_A)):
    for j in range(3):
        if wyckoff_A[i][j] < 0:
            wyckoff_A[i][j] = 1 + wyckoff_A[i][j]

# wycoff position of B, 4c
x_B = 1/4
y_B = 1/4
z_B = 1/4
wyckoff_B = [[1/4, 1/4, 1/4], [3/4, 3/4, 1/4],  [3/4, 1/4, 3/4], [1/4, 3/4, 3/4]]
for i in range(len(wyckoff_B)):
    for j in range(3):
        if wyckoff_B[i][j] < 0:
            wyckoff_B[i][j] = 1 + wyckoff_B[i][j]


# coordinate 
position_A = []
position_B = []

for i in range(int(size[0])):  
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_A)):
                temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                temp[0, 0] = (wyckoff_A[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_A[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_A[l][2] + k)/float(size[2]) 
                Ap = np.dot(l_cubic.T, temp) # 行列計算により絶対座標へ
                
                if Ap[0, 0] >= 0 and Ap[0, 0] <= l_cubic[0, 0]: # 
                    position_A.append("{} {} {}".format(Ap[0, 0], Ap[1, 0], Ap[2, 0]))
                    
for i in range(int(size[0])):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_B)):
                temp = np.zeros(shape=(3, 1))
                temp[0, 0] = (wyckoff_B[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_B[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_B[l][2] + k)/float(size[2])
                Bp = np.dot(l_cubic.T, temp)
                
                if Bp[0, 0] >= 0 and Bp[0, 0] <= l_cubic[0, 0]:
                    position_B.append("{} {} {}".format(Bp[0, 0], Bp[1, 0], Bp[2, 0]))

# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("sphalerite_{}_{}x{}x{}\n".format(atom_name[atomflag], size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_cubic[i][j]))
    f.write("\n")

for i in range(len(atom_list[atomflag])):
    f.write("{} ".format(atom_list[atomflag][i]))
f.write("\n")

f.write("{} {}\n".format(len(position_A), len(position_B)))
f.write("Cartesian\n")
for i in position_A:
    f.write(i + "\n")
for i in position_B:
    f.write(i + "\n")
f.close()
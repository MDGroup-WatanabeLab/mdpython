#Diamond C/Si/Ge/Sn
import os
import math
import numpy as np

# Parameters
atom_list = ["C", "Si", "Ge", "Sn"]
lattice_list = [3.56712, 5.431, 5.6754, 5.489]

print("Select atoms from following: ")
for i in range(len(atom_list)):
    print("{} : {}".format(i, atom_list[i]))
atomflag = int(input("Input number : "))


# input lattice size
while True:
    flag = 0
    size = input("Please input the lattice size [ x, y, z ] : ").split() # example : 3 3 3
    if len(size) == 3:
        for i in range(len(size)):
            if size[i].isdecimal() and int(size[i]) > 0:
                flag = 1
            else:
                flag = 0
                break
    if flag == 1:
        break


l_diamond = np.array([[lattice_list[atomflag] * float(size[0]), 0, 0], 
                    [0, lattice_list[atomflag] * float(size[1]), 0], 
                    [0, 0, lattice_list[atomflag] * float(size[2])]])


# wyckoff position 
x_diamond = 0.0
y_diamond = 0.0
z_diamond = 0.0
wyckoff_diamond = [[0.0, 0.0, 0.0], [0.0, 1/2, 1/2], [1/2, 0.0, 1/2], [1/2, 1/2, 0.0], [1/4, 1/4, 1/4], [3/4, 3/4, 1/4], [3/4, 1/4, 3/4], [1/4, 3/4, 3/4]]
for i in range(len(wyckoff_diamond)):
    for j in range(3):
        if wyckoff_diamond[i][j] < 0:
            wyckoff_diamond[i][j] = 1 + wyckoff_diamond[i][j]

# coordinate 
position_diamond = []

for i in range(int(size[0])):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_diamond)):
                temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                temp[0, 0] = (wyckoff_diamond[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_diamond[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_diamond[l][2] + k)/float(size[2]) 
                C = np.dot(l_diamond.T, temp) # 行列計算により絶対座標へ
                
                position_diamond.append("{} {} {}".format(C[0, 0], C[1, 0], C[2, 0]))

# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")

f.write("diamond_{}_{}x{}x{}\n".format(atom_list[atomflag], size[0], size[1], size[2]))

f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_diamond[i][j]))
    f.write("\n")
f.write("{}\n".format(atom_list[atomflag]))
f.write("{}\n".format(len(position_diamond)))
f.write("Cartesian\n")
for i in position_diamond:
    f.write(i + "\n")
f.close()


# rutile structure tetragonal
import os
import math
import numpy as np

# Parameters
atom_name = ["SiO2", "GeO2"]
atom_list = [["Si", "O"], ["Ge", "O"]]
lattice_list = [[4.1773, 4.1773, 2.6655], [4.41, 4.41, 2.88]]
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
l_tetragonal = np.array([[lattice_list[atomflag] * float(size[0]), 0, 0], 
                    [0, lattice_list[atomflag] * float(size[1]), 0], 
                    [0, 0, lattice_list[atomflag] * float(size[2])]])

if atomflag == 0:
    # wycoff position of A
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
                
else:  #GeO2, mp-470
    # wycoff position of A, 2a
    x_si = 1/2
    y_si = 1/2
    z_si = 1/2
    wyckoff_si = [[0, 0, 0], [1/2, 1/2, 1/2]]
    for i in range(len(wyckoff_si)):
        for j in range(3):
            if wyckoff_si[i][j] < 0:
                wyckoff_si[i][j] = 1 + wyckoff_si[i][j]

    # wycoff position of O, 4f 
    x_o = 0.694229
    y_o = 0.694229
    z_o = 0
    wyckoff_o= [[x_o, x_o, 0], [-x_o, -x_o, 0], [-x_o+1/2, x_o+1/2, 1/2], [x_o+1/2, -x_o+1/2, 1/2]]
    for i in range(len(wyckoff_o)):
        for j in range(3):
            if wyckoff_o[i][j] < 0:
                wyckoff_o[i][j] = 1 + wyckoff_o[i][j]



# coordinate 
position_A = []
position_B = []

for i in range(int(size[0])):  
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_si)):
                temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                temp[0, 0] = (wyckoff_si[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_si[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_si[l][2] + k)/float(size[2]) 
                si = np.dot(l_tetragonal.T, temp) # 行列計算により絶対座標へ
                position_A.append("{} {} {}".format(si[0, 0], si[1, 0], si[2, 0]))


for i in range(int(size[0])):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff_o)):
                temp = np.zeros(shape=(3, 1))
                temp[0, 0] = (wyckoff_o[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff_o[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff_o[l][2] + k)/float(size[2])
                o = np.dot(l_tetragonal.T, temp)
                position_B.append("{} {} {}".format(o[0, 0], o[1, 0], o[2, 0]))

# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("rutile_{}_{}x{}x{}\n".format(atom_name[atomflag], size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_tetragonal[i][j]))
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
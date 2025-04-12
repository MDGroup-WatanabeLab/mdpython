# fcc
import os
import math
import numpy as np

# Parameters
atom_list = ["Au", "Ag", "Cu", "Fe", "Al", "Co", "Ru", "Ni"]
lattice_list = [4.7825, 4.0862, 3.614967, 3.5910, 4.04958, 3.548, 3.79, 3.7836]

print("Select atoms from following: ")
for i in range(len(atom_list)):
    print("{} : {}".format(i, atom_list[i]))
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

# wyckoff position 
x = 0.0
y = 0.0
z = 0.0
wyckoff = [[0, 0, 0], [0, 1/2, 1/2], [1/2, 1/2, 0], [1/2, 0, 1/2]]
for i in range(len(wyckoff)):
    for j in range(3):
        if wyckoff[i][j] < 0:
            wyckoff[i][j] = 1 + wyckoff[i][j]



# coordinate 
position = []

for i in range(int(size[0])):
    for j in range(int(size[1])):
        for k in range(int(size[2])):
            for l in range(len(wyckoff)):
                temp = np.zeros(shape=(3, 1)) # 3行1列の要素が０の行列
                temp[0, 0] = (wyckoff[l][0] + i)/float(size[0])
                temp[1, 0] = (wyckoff[l][1] + j)/float(size[1])
                temp[2, 0] = (wyckoff[l][2] + k)/float(size[2]) 
                Ap = np.dot(l_cubic.T, temp) # 行列計算により絶対座標へ
                
                if Ap[0, 0] >= 0 and Ap[0, 0] <= l_cubic[0, 0] and Ap[0, 0] != lattice_list[atomflag]*float(size[0]): # 
                    position.append("{} {} {}".format(Ap[0, 0], Ap[1, 0], Ap[2, 0]))
                    


# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("fcc_{}_{}x{}x{}\n".format(atom_list[atomflag], size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_cubic[i][j]))
    f.write("\n")

f.write("{}\n".format(atom_list[atomflag]))

f.write("{}\n".format(len(position)))
f.write("C\n")
for i in position:
    f.write(i + "\n")

f.close()
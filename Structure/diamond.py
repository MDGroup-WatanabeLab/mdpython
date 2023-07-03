#Diamond C/Si/Ge/Sn
import os
import math
import numpy as np

# input atom
while True:
    atom = input("Select one atom name from C, Si, Ge and Sn : ")
    if atom != "C" and atom != "Si" and atom != "Ge" and atom != "Sn":
        print("ERROR : you select except C, Si, Ge and Sn !")
    else:
        break


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

if atom == "C":
# lattice parameter of unit cell C
    l_a = 3.56712
    l_b = 3.56712
    l_c = 3.56712

elif atom == "Si":
# lattice parameter of unit cell Si
    l_a = 5.431
    l_b = 5.431
    l_c = 5.431

elif atom == "Ge":
# lattice parameter of unit cell Ge
    l_a = 5.7871
    l_b = 5.7871
    l_c = 5.7871

elif atom == "Sn":
# lattice parameter of unit cell a-Sn
    l_a = 5.489
    l_b = 5.489
    l_c = 5.489

# lattice parameter (matrix format)
l_diamond = np.array([[l_a * float(size[0]), 0, 0], 
                    [0, l_b * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

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

if atom == "C":
    f.write("Diamond_C_{}x{}x{}\n".format(size[0], size[1], size[2]))
if atom == "SI":
    f.write("Diamond_Si_{}x{}x{}\n".format(size[0], size[1], size[2]))
if atom == "Ge":
    f.write("Diamond_Ge_{}x{}x{}\n".format(size[0], size[1], size[2]))
if atom == "Sn":
    f.write("Diamond_Sn_{}x{}x{}\n".format(size[0], size[1], size[2]))

f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_diamond[i][j]))
    f.write("\n")
f.write(atom + "\n")
f.write("{}\n".format(len(position_diamond)))
f.write("Cartesian\n")
for i in position_diamond:
    f.write(i + "\n")
f.close()


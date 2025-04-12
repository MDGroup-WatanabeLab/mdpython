import numpy as np
import re
import os 
import itertools
import matplotlib.pyplot as plt

# convert condition of z
min_z = 0.45
max_z = 0.55

# target file
f_format = ["POSCAR", "CONTCAR"]

# cutoff of bond length (by vesta)
max_bond_len = 2.8

# consider around original cell
"""
original cell : (x, y) = (0, 0)

  y
  ^
  |  ____________________________
  |  |        |        |        |
  |  |(-1, +1)|(0, +1) |(+1, +1)|
  |  |________|________|________|
  |  |        |        |        |
  |  |(-1, 0) | (0, 0) |(+1, 0) |
  |  |________|________|________|
  |  |        |        |        |
  |  |(-1, -1)|(0, -1) |(+1, -1)|
  |  |________|________|________|
  |
  |---------------------------> x

"""
consider = [0, 1, -1]
ppp = list(itertools.product(consider, repeat=2))

# output information
def add_info(ppp):
    info = "("
    xyz = ["x", "y", "z"]
    for i in range(len(ppp)):
        if i != 0:
            info += ", "
        
        info += xyz[i]
        if ppp[i] == 0:
            info += "0"
        elif ppp[i] == 1:
            info += "+"
        elif ppp[i] == -1:
            info += "-"
    info += ")"
    return info

# 
def coor_output(coor, ppp, lattice):
    x = float(coor[0]) + ppp[0]*float(lattice[0][0]) + ppp[1]*float(lattice[1][0])
    y = float(coor[1]) + ppp[0]*float(lattice[0][1]) + ppp[1]*float(lattice[1][1])
    z = coor[2]
    return [str(x), str(y), z]

# calculation a length between two atom
def bond_length(coor1, coor2, ppp, lattice):
    a = np.array([float(coor1[0]), float(coor1[1]), float(coor1[2])])
    b = np.array([float(coor2[0]) + ppp[0]*float(lattice[0][0]) + ppp[1]*float(lattice[1][0]), float(coor2[1]) + ppp[0]*float(lattice[0][1]) + ppp[1]*float(lattice[1][1]), float(coor2[2])])
    vec_a = a - b
    length_vec_a = np.linalg.norm(vec_a)
    return length_vec_a

# coor1 = atom a, coor2 = atom c, coor3 = atom b
# calculatino angle a-b-c
def bond_angle(coor1, coor2, coor3):
    a = np.array([float(coor1[0]), float(coor1[1]), float(coor1[2])])
    c = np.array([float(coor2[0]), float(coor2[1]), float(coor2[2])])
    b = np.array([float(coor3[0]), float(coor3[1]), float(coor3[2])])
    
    vec_a = a - b
    vec_c = c - b

    length_vec_a = np.linalg.norm(vec_a)
    length_vec_c = np.linalg.norm(vec_c)
    inner_product = np.inner(vec_a, vec_c)
    cos = inner_product / (length_vec_a * length_vec_c)
    
    rad = np.arccos(cos)
    degree = np.rad2deg(rad)
    return degree

# determine coordinate type
# The range is set from -1.1 to 1.1 because there were cases where 1 or -1 was exceeded despite relative coordinates
def coor_type(coordinate):
    count = 0
    for i in range(len(coordinate)):
        for j in range(3):
            if -1.1 <= float(coordinate[i][j]) <= 1.1:
                count += 1
    if count >= len(coordinate) * 2:
        return "Direct"
    else:
        return "Cartesian"

# convert coordinate (flag = 0 : from Direct to Cartesian, flag = 1 : from Cartesian to Direct)
def convert_coor(lattice, coordinate, flag):
    coor_coonverted = []
    if flag == 0:
        temp_coor = np.zeros(shape=(3, 1))
        temp_lattice = np.array([[float(lattice[0][0]), float(lattice[0][1]), float(lattice[0][2])], 
                                 [float(lattice[1][0]), float(lattice[1][1]), float(lattice[1][2])], 
                                 [float(lattice[2][0]), float(lattice[2][1]), float(lattice[2][2])]])
        for i in range(len(coordinate)):
            temp_coor[0, 0] = float(coordinate[i][0])
            temp_coor[1, 0] = float(coordinate[i][1])
            temp_coor[2, 0] = float(coordinate[i][2])
            cart = np.dot(temp_lattice.T, temp_coor)
            coor = [str(cart[0, 0]), str(cart[1, 0]), str(cart[2, 0])]
            coor_coonverted.append(coor)
        return coor_coonverted
    elif flag == 1:
        temp_coor = np.zeros(shape=(3, 1))
        temp_lattice = np.array([[float(lattice[0][0]), float(lattice[0][1]), float(lattice[0][2])], 
                                 [float(lattice[1][0]), float(lattice[1][1]), float(lattice[1][2])], 
                                 [float(lattice[2][0]), float(lattice[2][1]), float(lattice[2][2])]])
        for i in range(len(coordinate)):
            temp_coor[0, 0] = float(coordinate[i][0])
            temp_coor[1, 0] = float(coordinate[i][1])
            temp_coor[2, 0] = float(coordinate[i][2])
            cart = np.dot(np.linalg.inv(temp_lattice.T), temp_coor)
            coor = [str(cart[0, 0]), str(cart[1, 0]), str(cart[2, 0])]
            coor_coonverted.append(coor)     
        return coor_coonverted

# search file
path = os.getcwd()
dirlist = os.listdir(path)
file_list = []
for i in dirlist:
    flag = 0
    if os.path.isfile(i):
        for j in f_format:
            if re.search(j, i):
                flag = 1
    if flag == 1:
        file_list.append(i)
if len(file_list) == 0:
    print("There is no file")
    exit()

# select file
for i in range(len(file_list)):
    print(str(i) + " : " + file_list[i])
while True:
    num = input("Please select file : ")
    if num.isdecimal() and 0 <= int(num) < len(file_list):
        f_selected = file_list[int(num)]
        break

# open file
f = open(f_selected, "r")
line = f.readlines()
f.close()

# if "Selective dynamics" in the selected file
sd = 0
for i in line:
    if re.search("Selective dynamics", i):
        sd = 1

comment = []
lattice = []
atom_type = []
# si coordinate
coordinate1 = []
# o coordinate
coordinate2 = []

# scale
tmp = line[1].split()
if len(tmp) == 1:
    scale = [float(tmp[0]), float(tmp[0]), float(tmp[0])]
else:
    scale = [float(tmp[0]), float(tmp[1]), float(tmp[2])]

# lattice parameter
for i in range(2, 5):
    lattice.append(line[i].split())
for i in range(3):
    for j in range(3):
        lattice[i][j] = str(float(lattice[i][j]) * scale[j])
        
# atom type
atom_type = line[5].split()

# number of atom
atom_num = line[6].split()

print(line[7])

# coordinate
line_num = int(atom_num[0])
for i in range(8+sd, 8 + sd + line_num):
    if line[7+sd] == "Direct\n":
        print(i)
        if float(line[i].split()[2]) > min_z and float(line[i].split()[2]) < max_z:
            print(i)
            coordinate1.append(line[i].split())
        
    else:
        if float(line[i].split()[2]) > min_z*float(lattice[2][2]) and float(line[i].split()[2]) < max_z*float(lattice[2][2]):
            print(i)
            coordinate1.append(line[i].split())
    
    tmp = i

line_num = int(atom_num[1])
for i in range(tmp+1, tmp+1+line_num):
    if line[7+sd] == "Direct\n":
        if float(line[i].split()[2]) > min_z and float(line[i].split()[2]) < max_z:        
            print(i)
            coordinate2.append(line[i].split())
    else:
        if float(line[i].split()[2]) > min_z*float(lattice[2][2]) and float(line[i].split()[2]) < max_z*float(lattice[2][2]):        
            print(i)
            coordinate2.append(line[i].split())

# if coordinate is direct, change from direct to cartesian
if coor_type(coordinate1) == "Direct":
    coordinate1 = convert_coor(lattice, coordinate1, 0)
if coor_type(coordinate2) == "Direct":
    coordinate2 = convert_coor(lattice, coordinate2, 0)

# used for calculation of angle
angle_check = []
z_o = []
# used for output of angle information
elem_no = []
for i in range(len(coordinate1)):
    z_o.append(float(coordinate1[i][2]))
    bond_elem = []
    bond_elem.append(coordinate1[i] + ["Ge"+str(i+1)])
    for p in range(len(ppp)):
        for j in range(len(coordinate2)):
            if bond_length(coordinate1[i], coordinate2[j], ppp[p], lattice) < max_bond_len:
                tmp = coor_output(coordinate2[j], ppp[p], lattice)
                bond_elem.append(tmp + ["Ni"+str(j+1)+add_info(ppp[p])])
    # bond_elem includes coordinate of atom within the cutoff(=max_bond_len)
    # when calculatio angle, more than three atom coordinate
    if len(bond_elem) >= 3:
        angle_check.append(bond_elem)

# calculation angle
angle_data = []
depth_o = []
output = []
for i in range(len(angle_check)):
    # coordinate of O
    type1 = angle_check[i][0]
    # coordinate of Si within the cutoff(=max_bond_len)
    type2 = angle_check[i][1:]
    angle_set = list(itertools.combinations(type2, 2))
    for j in range(len(angle_set)):
        tmp = bond_angle(angle_set[j][0], angle_set[j][1], type1)
        angle_data.append(tmp)
        depth_o.append(float(type1[2])-min(z_o))
        output.append(angle_set[j][0][3] + " - " + type1[3] + " - " + angle_set[j][1][3] + " : " + str(tmp))
        
# output angle.txt 
with open("angle_" + str(f_selected) +".txt", "w") as f:
    print("Angle data : " + str(len(output)), file=f)
    
    for i in range(len(output)):
        print(output[i], file=f)
        
plt.figure()
bins = range(0, 180, 5)
plt.rcParams['font.family'] = 'Times New Roman'
plt.xlabel("Ni-Ge-Ni bond angle /dgree")
plt.ylabel("Frequency")
plt.hist(angle_data, bins, edgecolor="black")
plt.savefig("angle_" + str(f_selected) +".png")
plt.show()


"""
# incomplete code
plt.figure()
plt.rcParams['font.family'] = 'Times New Roman'
plt.xlabel("Oxigen distace from interface /angstrom")
plt.ylabel("Si-O-Si bond angle /dgree")
#plt.xlim(0, int(max(z_o)-min(z_o)), 2)
#plt.ylim(100, 180, 10)
plt.scatter(depth_o, angle_data)
plt.show()
"""

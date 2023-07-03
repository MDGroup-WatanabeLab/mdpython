import os
import re
import numpy as np
from pymatgen.core.periodic_table import Element

# Conversion to lmp format is basically unsupported
# It can be done, but some manual input may be required

f_format = ["mdl", "xyz", "lmp", "POSCAR"]
f_before = "" # file name before (include format)
format_after = ""  # file format after

# count atom number
def count_atom(atom_type):
    atom_num = []
    atom_el = sorted(set(atom_type), key = atom_type.index)
    for i in atom_el:
        atom_num.append(atom_type.count(i))
    return atom_num

# determine coordinate type
def coor_type(coordinate):
    count = 0
    for i in range(len(coordinate)):
        for j in range(3):
            if -1.1 <= float(coordinate[i][j]) <= 1.1:
                count += 1
    if count == len(coordinate) * 3:
        return "Direct"
    else:
        return "Cartesian"

# determine atom type from atom mass
def atom_type_check(weight):
    atom_mass = []
    atom_list = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", 
                 "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", 
                 "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", 
                 "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", 
                 "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", 
                 "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", 
                 "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
    for i in weight:
        for j in atom_list:
            atom_data = Element(j)
            m = str(atom_data.atomic_mass)
            m, _ = m.split()
            if m == i:
                atom_mass.append(j)
                break
    return atom_mass
            

# write mdl file
def convert_mdl(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate):
    flag = 0
    f = open(f_name + "." + format_after, "w")
    # fixed output
    f.write("Gear(5) RAND=10 ESWGE T=300.0 STEP=(0,1000100)\n")
    f.write("BLOCK FIXANGLE W=INF Q=INF LOGSTEP=10 PRINTVELOCITY dt=0.1fs scratch(100)\n")
    f.write("\n")
    for i in comment:
        if re.search("structure", i, re.IGNORECASE):
            f.write("{}".format(i))
            flag = 1
    if flag == 0:
        for i in atom_type:
            f.write(i + " ")
        f.write("structure\n")
    f.write("\n")
    
    # lattice parameter
    for i in range(3):
        for j in range(3):
            f.write(lattice[i][j] + " ")
        f.write("\n")
    f.write("\n")
    
    # If Cartesian relative coordinates, convert to relative coordinates
    if coor_type(coordinate) == "Cartesian":
        temp_coor = np.zeros(shape=(3, 1))
        temp_lattice = np.array([[float(lattice[0][0]), float(lattice[0][1]), float(lattice[0][2])], 
                                 [float(lattice[1][0]), float(lattice[1][1]), float(lattice[1][2])], 
                                 [float(lattice[2][0]), float(lattice[2][1]), float(lattice[2][2])]])
        for i in range(len(coordinate)):
            temp_coor[0, 0] = float(coordinate[i][0])
            temp_coor[1, 0] = float(coordinate[i][1])
            temp_coor[2, 0] = float(coordinate[i][2])
            cart = np.dot(np.linalg.inv(temp_lattice.T), temp_coor)
            coordinate[i][0] = str(cart[0, 0])
            coordinate[i][1] = str(cart[1, 0])
            coordinate[i][2] = str(cart[2, 0])    
            
    # write atom type and coordinate
    tmp = 0
    for i in range(len(atom_type)):
        num = tmp
        for j in range(num, num + int(atom_num[i])):
            f.write(atom_type[i] + " ")
            for k in range(3):
                f.write(coordinate[j][k] + " ")
            f.write("\n")
            tmp += 1
            
    f.close()

# write xyz file   
def convert_xyz(f_name, format_after, comment, lattice, atom_type, atom_num,coordinate):
    f = open(f_name + "." + format_after, "w")
    
    # write total number of atom
    num = 0
    for i in atom_num:
        num = num + int(i)
    f.write("{}\n".format(num))
    
    # fixed output
    flag = 0
    for i in comment:
        if re.search("structure", i, re.IGNORECASE):
            f.write("{}".format(i))
            flag = 1
    if flag == 0:
        for i in atom_type:
            f.write(i + " ")
        f.write("structure\n")
    
    # If relative coordinates, convert to Cartesian coordinates
    if coor_type(coordinate) == "Direct":
        temp_coor = np.zeros(shape=(3, 1))
        temp_lattice = np.array([[float(lattice[0][0]), float(lattice[0][1]), float(lattice[0][2])], 
                                 [float(lattice[1][0]), float(lattice[1][1]), float(lattice[1][2])], 
                                 [float(lattice[2][0]), float(lattice[2][1]), float(lattice[2][2])]])
        for i in range(len(coordinate)):
            temp_coor[0, 0] = float(coordinate[i][0])
            temp_coor[1, 0] = float(coordinate[i][1])
            temp_coor[2, 0] = float(coordinate[i][2])
            cart = np.dot(temp_lattice.T, temp_coor)
            coordinate[i][0] = str(cart[0, 0])
            coordinate[i][1] = str(cart[1, 0])
            coordinate[i][2] = str(cart[2, 0])
    
    # write atom type and coordinate
    tmp = 0
    for i in range(len(atom_type)):
        num = tmp
        for j in range(num, num + int(atom_num[i])):
            f.write(atom_type[i] + " ")
            for k in range(3):
                f.write(coordinate[j][k] + " ")
            f.write("\n")
            tmp += 1
            
    f.close()

# write lmp file  
def convert_lmp(f_name, format_after, comment, lattice, atom_type, atom_num,coordinate):
    f = open(f_name + "." + format_after, "w")
    
    # fixed output
    flag = 0
    for i in comment:
        if re.search("structure", i, re.IGNORECASE):
            f.write("{}".format(i))
            flag = 1
    if flag == 0:
        for i in atom_type:
            f.write(i + " ")
        f.write("structure\n")
    f.write("\n") 
    
    # write number of atom
    num = 0
    for i in atom_num:
        num = num + int(i)
    f.write(" {} atoms\n".format(num))
    
    # write number of atom type
    f.write(" {} atom types\n".format(len(atom_type)))
    
    # write lattice parameter
    f.write(" 0.00 {} xlo xhi\n".format(lattice[0][0]))
    f.write(" 0.00 {} ylo yhi\n".format(lattice[1][1]))
    f.write(" 0.00 {} zlo zhi\n".format(lattice[2][2]))
    f.write("\n")
    
    # write atom mass
    f.write(" Masses\n")
    f.write("\n")
    for i in range(len(atom_type)):
        atom_data = Element(atom_type[i])
        atom_mass = str(atom_data.atomic_mass)
        atom, _ = atom_mass.split()
        f.write("{} {}\n".format(i + 1, atom))
    f.write("\n")
    
    # ion
    atom_valence = []
    for i in range(len(atom_type)):
        atom_valence.append("ion{}".format(i + 1))
    
    # If relative coordinates, convert to Cartesian coordinates
    if coor_type(coordinate) == "Direct":
        temp_coor = np.zeros(shape=(3, 1))
        temp_lattice = np.array([[float(lattice[0][0]), float(lattice[0][1]), float(lattice[0][2])], 
                                 [float(lattice[1][0]), float(lattice[1][1]), float(lattice[1][2])], 
                                 [float(lattice[2][0]), float(lattice[2][1]), float(lattice[2][2])]])
        for i in range(len(coordinate)):
            temp_coor[0, 0] = float(coordinate[i][0])
            temp_coor[1, 0] = float(coordinate[i][1])
            temp_coor[2, 0] = float(coordinate[i][2])
            cart = np.dot(temp_lattice.T, temp_coor)
            coordinate[i][0] = str(cart[0, 0])
            coordinate[i][1] = str(cart[1, 0])
            coordinate[i][2] = str(cart[2, 0])
    
    # write coordinate
    f.write(" Atoms\n")
    f.write("\n")
    tmp = 0
    for i in range(len(atom_type)):
        num = tmp
        for j in range(num, num + int(atom_num[i])):
            tmp += 1  
            f.write("{} {} {} ".format(tmp, i + 1, atom_valence[i]))
            for k in range(3):
                f.write(coordinate[j][k] + " ")
            f.write("\n")  
            
    f.close()

# write POSCAR file  
def convert_POSCAR(f_name, format_after, comment, lattice, atom_type, atom_num,coordinate):
    f = open(format_after + "_" + f_name, "w")
    
    # fixed output
    flag = 0
    for i in comment:
        if re.search("structure", i, re.IGNORECASE):
            f.write("{}".format(i))
            flag = 1
    if flag == 0:
        for i in atom_type:
            f.write(i + " ")
        f.write("structure\n")
    
    # write lattice parameter
    f.write("1.0\n")
    for i in range(3):
        for j in range(3):
            f.write(lattice[i][j] + " ")
        f.write("\n")
    
    # write atom type and number of atom
    for i in atom_type:
        f.write(i + " ")
    f.write("\n")
    for i in atom_num:
        f.write(str(i) + " ")
    f.write("\n")
    
    # write coordinate type
    f.write(coor_type(coordinate) + "\n")
    
    # write coordinate
    for i in range(len(coordinate)):
        for j in range(3):
            f.write(coordinate[i][j] + " ")
        f.write("\n")
                
    f.close()

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
    print("Their is no file")
    exit()

# select file
f_name = ""
for i in range(len(file_list)):
    print(str(i) + " : " + file_list[i])
while True:
    num = input("Please select a file to change format from above : ")
    if num.isdecimal() and 0 <= int(num) < len(file_list):
        f_before = file_list[int(num)]
        break
    
# select format
for i in range(len(f_format)):
    print(str(i) + " : " + f_format[i])
while True:
    num = input("Which format do you want to convert to? : ")
    if num.isdecimal() and 0 <= int(num) < len(f_format) and f_format[int(num)] not in f_before:
        format_after = f_format[int(num)]
        break

# input file name
while True:
    err = 0
    f_name = input("Please input the name of the converted file: ")
    if f_name != "":
        for i in file_list:
            if f_name + "." + format_after == i:
                print("{}.{} already exists".format(f_name, format_after))
                err += 1
        if err == 0:
            break

# read file
f = open(f_before, "r")
line = f.readlines()
f.close()

# data
comment = []
lattice = []
atom_type = []
coordinate = []

# get data
if re.search("mdl", f_before):
    for i in range(5):
        comment.append(line[i])
    for i in range(5, 8):
        lattice.append(line[i].split())
    for i in range(9, len(line)):
        atom, *coor = line[i].split()
        atom_type.append(atom)
        coordinate.append(coor)
    atom_num = count_atom(atom_type)
    atom_type = sorted(set(atom_type), key = atom_type.index)
    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))
elif re.search("xyz", f_before):
    print("No lattice constants, it is not possible to convert from the xyz file to another file")
    exit()
    comment.append(line[1])
    lattice = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
    for i in range(2, len(line)):
        atom, *coor = line[i].split()
        atom_type.append(atom)
        coordinate.append(coor)   
    atom_num = count_atom(atom_type)
    atom_type = sorted(set(atom_type), key = atom_type.index)   
    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))
elif re.search("lmp", f_before):
    comment.append(line[0])
    x = line[4].split()
    y = line[5].split()
    z = line[6].split()
    lattice = [[x[1], "0", "0"], ["0", y[1], "0"], ["0", "0", z[1]]]
    type_num, *_= line[3].split()
    for i in range(10 + 3 + int(type_num), len(line)):
        _, atom, _, *coor = line[i].split()
        atom_type.append(atom)
        coordinate.append(coor)
    atom_num = count_atom(atom_type)
    atom_type = sorted(set(atom_type), key = atom_type.index)
    weight = []
    for i in range(10, 10 + len(atom_type)):
        _, m = line[i].split()
        weight.append(m)
    atom_type = atom_type_check(weight)
    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))
elif re.search("POSCAR", f_before):
    comment.append(line[0])
    scale = float(line[1])
    for i in range(2, 5):
        lattice.append(line[i].split())
    for i in range(3):
        for j in range(3):
            lattice[i][j] = str(float(lattice[i][j]) * scale)
    atom_type = line[5].split()
    atom_num = line[6].split()
    for i in range(8, len(line)):
        coordinate.append(line[i].split())       
    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))

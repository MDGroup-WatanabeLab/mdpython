import os
import re
import numpy as np
from pymatgen.core.periodic_table import Element

# file format
f_format = ["mdl", "lmp", "POSCAR"]

# float type or not
def is_float(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

# sort atom type
def sort_atom_type(atom_type):
    atom_types = []
    atom = sorted(set(atom_type), key = atom_type.index)
    for i in atom:
        for j in atom_type:
            if i == j:
                atom_types.append(j)
    return atom_types

# sort coordinate by atom type
def sort_coordinate(coordinate, atom_type):
    atom = sorted(set(atom_type), key = atom_type.index)
    coor = []
    for i in atom:
        for j in range(len(atom_type)):
            if i == atom_type[j]:
                coor.append(coordinate[j])      
    return coor

# sort ion ("ion" represents the value in the third column of lmp file)
def sort_ion(ion, atom_type):
    atom = sorted(set(atom_type), key = atom_type.index)
    atom_ion = []
    for i in atom:
        for j in range(len(atom_type)):
            if i == atom_type[j]:
                atom_ion.append(ion[j]) 
    return atom_ion

# determine lattice paramter
# adopt the samller lattice paramter
def choice_lattice(lattice1, lattice2, direction, stack_gap):
    lattice = [["0", "0", "0"], 
               ["0", "0", "0"], 
               ["0", "0", "0"]]
    if direction == "x":
        lattice[0][0] = str(float(lattice1[0][0]) + float(lattice2[0][0]) + stack_gap)
        lattice[1][1] = str(max(float(lattice1[1][1]), float(lattice2[1][1])))
        lattice[2][2] = str(max(float(lattice1[2][2]), float(lattice2[2][2])))
    elif direction == "y":
        lattice[1][1] = str(float(lattice1[1][1]) + float(lattice2[1][1]) + stack_gap)       
        lattice[0][0] = str(max(float(lattice1[0][0]), float(lattice2[0][0])))
        lattice[2][2] = str(max(float(lattice1[2][2]), float(lattice2[2][2])))
    elif direction == "z":
        lattice[2][2] = str(float(lattice1[2][2]) + float(lattice2[2][2]) + stack_gap)  
        lattice[0][0] = str(max(float(lattice1[0][0]), float(lattice2[0][0])))
        lattice[1][1] = str(max(float(lattice1[1][1]), float(lattice2[1][1])))
    return lattice

# change coordinate (add lattice paramter to coordinate of second structure)
def coordinate_change(coordinate2, lattice1, direction, stack_gap):
    for i in range(len(coordinate2)):
        if direction == "x":
            coordinate2[i][0] = str(float(coordinate2[i][0]) + float(lattice1[0][0]) + stack_gap)
        elif direction == "y":
            coordinate2[i][1] = str(float(coordinate2[i][1]) + float(lattice1[1][1]) + stack_gap)
        elif direction == "z":
            coordinate2[i][2] = str(float(coordinate2[i][2]) + float(lattice1[2][2]) + stack_gap)
    return coordinate2

# remove atoms outside the lattice
def remove_atom(lattice, coordinate, direction):
    re_atom = []
    for i in range(len(coordinate)):
        if direction == "x":
            if float(coordinate[i][1]) > float(lattice[1][1]) or float(coordinate[i][2]) > float(lattice[2][2]):
                re_atom.append(i)
        if direction == "y":
            if float(coordinate[i][0]) > float(lattice[0][0]) or float(coordinate[i][2]) > float(lattice[2][2]):
                re_atom.append(i)
        if direction == "z":
            if float(coordinate[i][0]) > float(lattice[0][0]) or float(coordinate[i][1]) > float(lattice[1][1]):
                re_atom.append(i)               
    return re_atom

# remove atoms outside from the lattice
def remove_coordinate(coordinate, re_atom):
    coor = []
    for i in range(len(coordinate)):
        if i not in re_atom:
            coor.append(coordinate[i])
    return coor

# remove atoms outside from the lattice
def remove_atom_type(atom_type, re_atom):
    atom = []
    for i in range(len(atom_type)):
        if i not in re_atom:
            atom.append(atom_type[i])
    return atom

# remove atoms outside from the lattice (use when you select lmp file)
def remove_ion(ion, re_atom):
    atom_ion = []
    for i in range(len(ion)):
        if i not in re_atom:
            atom_ion.append(ion[i])
    return atom_ion   

# count the number of atom
def count_atom(atom_type):
    atom_num = []
    atom_el = sorted(set(atom_type), key = atom_type.index)
    for i in atom_el:
        atom_num.append(atom_type.count(i))
    return atom_num

# determine coordinate type
# The range is set from -1.1 to 1.1 because there were cases where 1 or -1 was exceeded despite relative coordinates
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

# determine atom type from atom mass (when you select lmp file)
def atom_type_check(weight, atom_list):
    atom_mass = []
    for i in weight:
        for j in atom_list:
            atom_data = Element(j)
            m = str(atom_data.atomic_mass)
            m, _ = m.split()
            if m == i:
                atom_mass.append(j)
                break
    return atom_mass

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

# write mdl file
def convert_mdl(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate):
    flag = 0
    f = open(f_name + format_after, "w")
    
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
    
    # write lattice parameter
    for i in range(3):
        for j in range(3):
            f.write(lattice[i][j] + " ")
        f.write("\n")
    f.write("\n")
    
    # If Cartesian relative coordinates, convert to relative coordinates
    if coor_type(coordinate) == "Cartesian":
        coordinate = convert_coor(lattice, coordinate, 1)  
     
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
def convert_lmp(f_name, format_after, comment, lattice, atom_type, atom_num, ion, coordinate):
    f = open(f_name + format_after, "w")
    
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
    
    # If relative coordinates, convert to Cartesian coordinates
    if coor_type(coordinate) == "Direct":
        coordinate = convert_coor(lattice, coordinate, 0)
    
    # write coordinate
    f.write(" Atoms\n")
    f.write("\n")
    tmp = 0
    for i in range(len(atom_type)):
        num = tmp
        for j in range(num, num + int(atom_num[i])):
            tmp += 1  
            f.write("{} {} {} ".format(tmp, i + 1, ion[j]))
            for k in range(3):
                f.write(coordinate[j][k] + " ")
            f.write("\n")  
            
    f.close()

# write POSCAR file  
def convert_POSCAR(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate):
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

# list of chemical symbol
atom_list = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", 
             "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", 
             "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", 
             "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", 
             "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", 
             "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", 
             "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]

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

# select 1st file
for i in range(len(file_list)):
    print(str(i) + " : " + file_list[i])
while True:
    num = input("Please select 1st file : ")
    if num.isdecimal() and 0 <= int(num) < len(file_list):
        f_1st = file_list[int(num)]
        if "POSCAR" not in f_1st:
            f1_format = os.path.splitext(f_1st)[1]
            break
        else:
            f1_format = "POSCAR"
            break

# select 2nd file
while True:
    num = input("Please select 2nd file : ")
    if num.isdecimal() and 0 <= int(num) < len(file_list):
        f_2nd = file_list[int(num)]
        if "POSCAR" not in f_2nd:
            f2_format = os.path.splitext(f_2nd)[1]
        else:
            f2_format = "POSCAR"
        if f_2nd == f_1st:
            print("Can't select same file")
        elif f1_format != f2_format:
            print("Can't select different format of file")
        else:
            break

# input direction to stack
while True:
    direction = input("Please input direction to stack : ")
    if direction == "x" or direction == "y" or direction == "z":
        break

# input the distance between 1st structure and 2nd structure
while True:
    stack_gap = input("Please select distance among two structure : ")
    if is_float(stack_gap) and 0 <= float(stack_gap):
        stack_gap = float(stack_gap)
        break

# input file name
while True:
    err = 0
    f_name = input("Please input the name of the converted file: ")
    if f_name != "":
        for i in file_list:
            if f_name + "." + f1_format == i:
                print("{}{} already exists".format(f_name, f1_format))
                err += 1
        if err == 0:
            break

# read 1st and 2nd file
f1 = open(f_1st, "r")
line1 = f1.readlines()
f1.close()

f2 = open(f_2nd, "r")
line2 = f2.readlines()
f2.close()

# data
comment1 = []
comment2 = []
lattice1 = []
lattice2 = []
atom_type1 = []
atom_type2 = []
coordinate1 = []
coordinate2 = []

comment = []
lattice = []
atom_type = []
coordinate = []

# get data
if re.search("mdl", f1_format):
    # get comment
    for i in range(5):
        comment1.append(line1[i])
        
    # get lattice parameter
    for i in range(5, 8):
        lattice1.append(line1[i].split())
        
    # get atom type and coordinate
    for i in range(9, len(line1)):
        atom, *coor = line1[i].split()
        atom_type1.append(atom)
        coordinate1.append(coor)
    
    # convert to cartesian coordinate
    if coor_type(coordinate1) == "Direct":
        coordinate1 = convert_coor(lattice1, coordinate1, 0)
    
    # get comment
    for i in range(5):
        comment2.append(line2[i])
        
    # get lattice parameer
    for i in range(5, 8):
        lattice2.append(line2[i].split())
        
    # get atom type and coordinate
    for i in range(9, len(line2)):
        atom, *coor = line2[i].split()
        atom_type2.append(atom)
        coordinate2.append(coor)
        
    # convert to cartesian coordinate
    if coor_type(coordinate2) == "Direct":
        coordinate2 = convert_coor(lattice2, coordinate2, 0)
        
    # determine lattice
    lattice = choice_lattice(lattice1, lattice2, direction, stack_gap)
    
    # change coordinate
    coordinate2 = coordinate_change(coordinate2, lattice1, direction, stack_gap)

    # combine data of two structure into one array
    atom_type = atom_type1 + atom_type2  
    coordinate = coordinate1 + coordinate2
    
    # sort coordinate because coordinate of different atoms is mixed
    coordinate = sort_coordinate(coordinate, atom_type)
    
    # sort atom type to suit sorted coordinate
    atom_type = sort_atom_type(atom_type)  
    
    # remove atoms outside the lattice
    re_atom = remove_atom(lattice, coordinate, direction)
    coordinate = remove_coordinate(coordinate, re_atom)
    atom_type = remove_atom_type(atom_type, re_atom)
    
    # count the number of atom
    atom_num = count_atom(atom_type)
    
    # get atom type
    atom_type = sorted(set(atom_type), key = atom_type.index)
    
    convert_mdl(f_name, f1_format, comment, lattice, atom_type, atom_num, coordinate)
    
elif re.search("lmp", f1_format):
    ion1 = []
    ion2 = []
    
    # get comment
    comment1.append(line1[0])
    
    # get lattice parameter
    x = line1[4].split()
    y = line1[5].split()
    z = line1[6].split()
    lattice1 = [[str(float(x[1]) - float(x[0])), "0", "0"], ["0", str(float(y[1]) - float(y[0])), "0"], ["0", "0", str(float(z[1]) - float(z[0]))]]
    
    # get atom type, ion and coordinate
    type_num, *_= line1[3].split()
    for i in range(10 + 3 + int(type_num), len(line1)):
        _, atom, ion, *coor = line1[i].split()
        atom_type1.append(atom)
        coordinate1.append(coor)
        ion1.append(ion)
    
    # get comment
    comment2.append(line1[0])
    
    # get atom type, ion and coordinate
    x = line2[4].split()
    y = line2[5].split()
    z = line2[6].split()
    lattice2 = [[str(float(x[1]) - float(x[0])), "0", "0"], ["0", str(float(y[1]) - float(y[0])), "0"], ["0", "0", str(float(z[1]) - float(z[0]))]]
    type_num, *_= line2[3].split()
    for i in range(10 + 3 + int(type_num), len(line2)):
        _, atom, ion, *coor = line2[i].split()
        atom_type2.append(atom)
        coordinate2.append(coor)
        ion2.append(ion) 
    
    # determine lattice
    lattice = choice_lattice(lattice1, lattice2, direction, stack_gap)
    
    # change coordinate
    coordinate2 = coordinate_change(coordinate2, lattice1, direction, stack_gap)

    # combine data of two structure into one array
    coordinate = coordinate1 + coordinate2
    atom_type = atom_type1 + atom_type2
    ion = ion1 + ion2
    
    # sort coordinate because coordinate of different atoms is mixed
    coordinate = sort_coordinate(coordinate, atom_type)
    
    # sort ion because ion of different atoms is mixed
    ion = sort_ion(ion, atom_type)
    
    # sort atom type to suit sorted coordinate
    atom_type = sort_atom_type(atom_type)
    
    # remove atoms outside the lattice
    re_atom = remove_atom(lattice, coordinate, direction)
    coordinate = remove_coordinate(coordinate, re_atom)
    atom_type = remove_atom_type(atom_type, re_atom)
    ion = remove_ion(ion, re_atom)
    
    # count the number of atom
    atom_num = count_atom(atom_type)
    
    # get atom type
    atom_type = sorted(set(atom_type), key = atom_type.index)

    convert_lmp(f_name, f1_format, comment, lattice, atom_type, atom_num, ion, coordinate)

elif re.search("POSCAR", f1_format):
    # get comment
    comment1.append(line1[0])
    
    # get scale of lattice
    scale = float(line1[1])
    
    # get lattice parameter
    for i in range(2, 5):
        lattice1.append(line1[i].split())
    for i in range(3):
        for j in range(3):
            lattice1[i][j] = str(float(lattice1[i][j]) * scale)
    
    # get atom type
    atom_type1 = line1[5].split()
    
    # get the number of atom
    atom_num1 = line1[6].split()
    
    # get coordinate
    line_num = 0
    for i in atom_num1:
        line_num = line_num + int(i)
    for i in range(8, 8 + line_num):
        coordinate1.append(line1[i].split())   
    
    # convert to cartesian coordinate
    if coor_type(coordinate1) == "Direct":
        coordinate1 = convert_coor(lattice1, coordinate1, 0)
        
    # get comment
    comment2.append(line2[0])
    
    # get scale of lattice
    scale = float(line2[1])
    
    # get lattice parameter
    for i in range(2, 5):
        lattice2.append(line2[i].split())
    for i in range(3):
        for j in range(3):
            lattice2[i][j] = str(float(lattice2[i][j]) * scale)
            
    # get atom type
    atom_type2 = line2[5].split()
    
    # get the number of atom
    atom_num2 = line2[6].split()
    
    # get coordinate
    line_num = 0
    for i in atom_num2:
        line_num = line_num + int(i)
    for i in range(8, 8 + line_num):
        coordinate2.append(line2[i].split())   
    
    # convert to cartesian coordinate
    if coor_type(coordinate2) == "Direct":
        coordinate2 = convert_coor(lattice2, coordinate2, 0)  
    
    # determine lattice    
    lattice = choice_lattice(lattice1, lattice2, direction, stack_gap)
    
    # change coordinate
    coordinate2 = coordinate_change(coordinate2, lattice1, direction, stack_gap)
    
    # combine data of two structure into one array
    coordinate = coordinate1 + coordinate2
    for i in range(len(atom_type1)):
        for j in range(int(atom_num1[i])):
            atom_type.append(atom_type1[i])
    for i in range(len(atom_type2)):
        for j in range(int(atom_num2[i])):
            atom_type.append(atom_type2[i])
    
    # sort coordinate because coordinate of different atoms is mixed 
    coordinate = sort_coordinate(coordinate, atom_type)
    
    # sort atom type to suit sorted coordinate
    atom_type = sort_atom_type(atom_type)  
    
    # remove atoms outside the lattice
    re_atom = remove_atom(lattice, coordinate, direction)
    coordinate = remove_coordinate(coordinate, re_atom)
    atom_type = remove_atom_type(atom_type, re_atom)
    
    # count the number of atom
    atom_num = count_atom(atom_type)
    
    # get atom type
    atom_type = sorted(set(atom_type), key = atom_type.index)
    
    convert_POSCAR(f_name, f1_format, comment, lattice, atom_type, atom_num, coordinate)    
    
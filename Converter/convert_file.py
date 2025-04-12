import os
import re
import numpy as np
import math
from pymatgen.core.periodic_table import Element

# Conversion to lmp format is basically unsupported
# It can be done, but some manual input may be required

# file format before conversion (for searching file)
f_format = ["mdl", "xyz", "lmp", "final", "POSCAR", "CONTCAR"]

# convertibel format
format_conv = ["mdl", "xyz", "lmp", "POSCAR"]

# check interger or not
def is_integer(n):
    if n == "none":
        return True
    else:        
        try:
            int(n)
        except Exception:
            return False
        else:
            return True

# input atom type (when you select final file as file before conversion)
def id_atom(atom_type, atom_list):
    atom = []
    for i in atom_type:
        id = input("Please input atom of id {} : ".format(i))
        while True:
            if id.lower().title() in atom_list:
                atom.append(id.lower().title())
                break
    return atom

# count atom number by type
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
    if count >= len(coordinate) * 2:
        return "Direct"
    else:
        return "Cartesian"

# determine atom type from atom mass (when you select lmp file as file before conversion)
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

# added by nishimura
def is_orthogonal(basis):
    # 与えられた基底ベクトルをNumPy配列に変換
    basis = np.array(basis, dtype=np.float64)

    # 基底ベクトルの内積を計算
    dot_products = np.dot(basis, basis.T)

    # 内積行列の対角成分を0と比較
    is_orthogonal = np.allclose(dot_products - np.diag(np.diag(dot_products)), 0)

    return is_orthogonal

# added by nishimura 
# convert lattice parameter 
# reference : https://docs.lammps.org/Howto_triclinic.html
def convert_basis(basis):
    basis = np.array([[float(basis[0][0]), float(basis[0][1]), float(basis[0][2])],
                      [float(basis[1][0]), float(basis[1][1]), float(basis[1][2])],
                      [float(basis[2][0]), float(basis[2][1]), float(basis[2][2])]])

    num_basis, dim = basis.shape

    lengths = np.linalg.norm(basis, axis=1)

    unit_basis = basis / lengths[:, np.newaxis]

    angles = np.zeros((num_basis, num_basis))
    for i in range(num_basis):
        for j in range(i + 1, num_basis):
            angle = np.arccos(np.dot(unit_basis[i], unit_basis[j]))
            angles[i][j] = angle
            angles[j][i] = angle

    A, B, C = lengths[0], lengths[1], lengths[2]
    alpha ,beta, gamma = angles[1][2], angles[0][2], angles[0][1]

    ax = A
    bx = B * math.cos( gamma )
    by = B * math.sin( gamma )
    cx = C * math.cos( beta )
    cy = ( B * C * math.cos( alpha ) - bx * cx ) / by
    cz = np.sqrt( C ** 2 - cx ** 2 - cy ** 2 )
    converted_basis =[[ax, bx, cx],
                      [0, by, cy],
                      [0, 0, cz]]

    return converted_basis

# convert coordinate for lmp
# reference : https://docs.lammps.org/Howto_triclinic.html
def convert_coor_for_lmp(lattice, coordinate, changed_lattice):
    coor = [] 
    changed_basis = np.array([[changed_lattice[0][0], changed_lattice[0][1], changed_lattice[0][2]], 
                              [changed_lattice[1][0], changed_lattice[1][1], changed_lattice[1][2]], 
                              [changed_lattice[2][0], changed_lattice[2][1], changed_lattice[2][2]]])
    A = np.array([float(lattice[0][0]), float(lattice[0][1]), float(lattice[0][2])])
    B = np.array([float(lattice[1][0]), float(lattice[1][1]), float(lattice[1][2])])
    C = np.array([float(lattice[2][0]), float(lattice[2][1]), float(lattice[2][2])])
    
    Volume = abs(np.dot(np.cross(A, B), C))
    
    tmp_array = np.array([[np.cross(B, C)[0], np.cross(B, C)[1], np.cross(B, C)[2]], 
                          [np.cross(C, A)[0], np.cross(C, A)[1], np.cross(C, A)[2]],
                          [np.cross(A, B)[0] , np.cross(A, B)[1], np.cross(A, B) [2]]])
    tmp_array = tmp_array / Volume

    for i in range(len(coordinate)):
        coor_before = np.array([[float(coordinate[i][0])], [float(coordinate[i][1])], [float(coordinate[i][2])]])
        coor_after = np.dot(np.dot(changed_basis, tmp_array), coor_before)
        tmp_coor = [coor_after[0][0], coor_after[1][0], coor_after[2][0]]
        coor.append(tmp_coor)
    
    return coor

# convert coordinate (flag = 0 : from Direct to Cartesian, flag = 1 : from Cartesian to Direct)
def convert_coor(lattice, coordinate, flag):
    coor_converted = []
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
            coor_converted.append(coor)
        return coor_converted
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
            coor_converted.append(coor)
        return coor_converted

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

# write xyz file
def convert_xyz(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate):
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
        coordinate = convert_coor(lattice, coordinate, 0)

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
def convert_lmp(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate):
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
    if is_orthogonal(lattice):
        f.write(" 0.00 {} xlo xhi\n".format(lattice[0][0]))
        f.write(" 0.00 {} ylo yhi\n".format(lattice[1][1]))
        f.write(" 0.00 {} zlo zhi\n".format(lattice[2][2]))
        f.write("\n")
    else:
        changed_basis = convert_basis(lattice)
        xhi = changed_basis[0][0]
        yhi = changed_basis[1][1]
        zhi = changed_basis[2][2]
        xy = changed_basis[0][1]
        xz = changed_basis[0][2]
        yz = changed_basis[1][2]
        f.write(" 0.00 {} xlo xhi\n".format(xhi))
        f.write(" 0.00 {} ylo yhi\n".format(yhi))
        f.write(" 0.00 {} zlo zhi\n".format(zhi))
        f.write(" {} {} {} xy xz yz\n".format(xy ,xz ,yz))
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

    # ion (this part depend on type of lmp file)
    atom_valence = []
    for i in range(len(atom_type)):
        while True:
            ion_n = input("Please input charge of {} (If not necessary, input \"none\"): ".format(atom_type[i]))
            if is_integer(ion_n):
                atom_valence.append(ion_n)
                break

    # If relative coordinates, convert to Cartesian coordinates
    if is_orthogonal(lattice):
        if coor_type(coordinate) == "Direct":
            coordinate = convert_coor(lattice, coordinate, 0)
    else:
        if coor_type(coordinate) == "Direct":
            coordinate = convert_coor(lattice, coordinate, 0)
            coordinate = convert_coor_for_lmp(lattice, coordinate, changed_basis)

    # write coordinate
    f.write(" Atoms\n")
    f.write("\n")
    tmp = 0
    for i in range(len(atom_type)):
        num = tmp
        for j in range(num, num + int(atom_num[i])):
            tmp += 1
            if atom_valence[i] == "none":
                f.write("{} {} ".format(tmp, i+1))
            else:
                f.write("{} {} {} ".format(tmp, i+1, atom_valence[i]))
            for k in range(3):
                f.write(str(coordinate[j][k]) + " ")
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

# select file
for i in range(len(file_list)):
    print(str(i) + " : " + file_list[i])
while True:
    num = input("Please select a file to change format from above : ")
    if num.isdecimal() and 0 <= int(num) < len(file_list):
        f_before = file_list[int(num)]
        break

# select format
for i in range(len(format_conv)):
    print(str(i) + " : " + format_conv[i])
while True:
    num = input("Which format do you want to convert to? : ")
    if num.isdecimal() and 0 <= int(num) < len(format_conv) and format_conv[int(num)] not in f_before:
        format_after = format_conv[int(num)]
        break

# input converted file name
while True:
    err = 0
    f_name = input("Please input the name of the converted file: ")
    if f_name != "":
        for i in file_list:
            if format_after != "POSCAR" or format_after == "CONTCAR":
                if f_name + "." + format_after == i:
                    print("{}.{} already exists".format(f_name, format_after))
                    err = 1
            else:
                if f_name + "_" + format_after == i:
                    print("{}_{} already exists".format(f_name, format_after))
                    err = 1
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
    # get comment
    for i in range(5):
        comment.append(line[i])

    # get lattice parameter
    for i in range(5, 8):
        lattice.append(line[i].split())

    # get atom type and coordinate
    for i in range(9, len(line)):
        atom, *coor = line[i].split()
        atom_type.append(atom)
        coordinate.append(coor)

    # count the number of atom by type
    atom_num = count_atom(atom_type)

    # get type of atom
    atom_type = sorted(set(atom_type), key = atom_type.index)

    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))

elif re.search("xyz", f_before):
    # xyz file has no lattice parameter so the xyz file can not convert to another file
    print("No lattice constants, it is not possible to convert from the xyz file to another file")
    exit()

    # if you convert to another file, you have to determine lattice parameter
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
    # get comment
    comment.append(line[0])
    
    for i in range(len(line)):
        if re.search("xlo", line[i]):
            flag_l = i
            break

    # get lattice paramter
    if len(line[flag_l+3].split()) == 0:
        x = line[flag_l].split()
        y = line[flag_l+1].split()
        z = line[flag_l+2].split()
        lattice = [[str(float(x[1]) - float(x[0])), "0", "0"], ["0", str(float(y[1]) - float(y[0])), "0"], ["0", "0", str(float(z[1]) - float(z[0]))]]
        flag_l += 2
    else:
        x = line[flag_l].split()
        y = line[flag_l+1].split()
        z = line[flag_l+2].split()
        xy, xz, yz, *_ = line[flag_l+3].split()
        lattice = [[str(float(x[1]) - float(x[0])), "0", "0"], [xy, str(float(y[1]) - float(y[0])), "0"], [xz, yz, str(float(z[1]) - float(z[0]))]]  
        flag_l += 3 

    # get atom type and coordinate
    type_num, *_= line[3].split()
    for i in range(flag_l + 3 + int(type_num) + 4, len(line)):
        _, atom, *coor = line[i].split()
        atom_type.append(atom)
        coordinate.append(coor)

    # count the number of atom by type
    atom_num = count_atom(atom_type)

    # get type of atom
    atom_type = sorted(set(atom_type), key = atom_type.index)

    # get chemical symbol from weight
    weight = []
    for i in range(flag_l + 4, flag_l + 4 + len(atom_type)):
        _, *m = line[i].split()
        weight.append(m[0])
    atom_type = atom_type_check(weight, atom_list)
    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))

elif re.search("final", f_before):
    # get lattice parameter
    x = line[5].split()
    y = line[6].split()
    z = line[7].split()
    xlo = float(x[0]) - min(0.0, float(x[2]), float(y[2]), float(x[2]) + float(y[2]))
    xhi = float(x[1]) - max(0.0, float(x[2]), float(y[2]), float(x[2]) + float(y[2]))
    ylo = float(y[0]) - min(0.0, float(z[2]))
    yhi = float(y[1]) - max(0.0, float(z[2]))
    lattice = [[str(float(xhi) - float(xlo)), "0", "0"], [x[2], str(float(y[1]) - float(y[0])), "0"], [y[2], z[2], str(float(z[1]) - float(z[0]))]]

    # get atom type
    for i in range(9, len(line)):
        # _, atom, *_ = line[i].split()
        atom, *_ = line[i].split()
        atom_type.append(atom)

    # count the number of atom by type
    atom_num = count_atom(atom_type)

    # get type of atom
    atom_type = sorted(set(atom_type), key = atom_type.index)
    
    # get coordinate
    for i in atom_type:
        for j in range(9, len(line)):
            # _, atom, *coor = line[j].split()
            atom, coor_x, coor_y, coor_z, *_ = line[j].split()
            coor = [coor_x, coor_y, coor_z]
            if atom == i:
                coordinate.append(coor)
    
    # input chemical symbol
    atom_type = id_atom(atom_type, atom_list)

    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))

elif re.search("POSCAR", f_before) or re.search("CONTCAR", f_before):
    # get comment
    comment.append(line[0])

    # get scale of lattice and lattice parameter
    scale = float(line[1])
    for i in range(2, 5):
        lattice.append(line[i].split())
    for i in range(3):
        for j in range(3):
            lattice[i][j] = str(float(lattice[i][j]) * scale)

    # get atom type
    atom_type = line[5].split()

    # get the number of atom by type
    atom_num = line[6].split()
    
    sd = 0
    if re.search("Selective dynamics", line[7]):
        sd = 1
    # get coordinate
    line_num = 0
    for i in atom_num:
        line_num = line_num + int(i)
    for i in range(8+sd, 8 + sd + line_num):
        tmp_line = line[i].split()
        tmp_coor = [tmp_line[0], tmp_line[1], tmp_line[2]]
        coordinate.append(tmp_coor)
    exec("convert_{}(f_name, format_after, comment, lattice, atom_type, atom_num, coordinate)".format(format_after))

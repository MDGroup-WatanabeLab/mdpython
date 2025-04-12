import re
import numpy as np

freq = 100
counter_b = 0
counter_e = 0
counter_p = 0
counter_s = 0
counter_f = 0
lattice_count = 0

def convert_coor(lattice, coordinate, flag):
    coor_coonverted = []

    # tmp_coor = [x, y, z]^T, tmp_latticeは格子定数
    if flag == 0:
        tmp_coor = np.zeros(shape=(3, 1))
        tmp_lattice = np.array([[float(lattice[0][0]), float(lattice[0][1]), float(lattice[0][2])], 
                                 [float(lattice[1][0]), float(lattice[1][1]), float(lattice[1][2])], 
                                 [float(lattice[2][0]), float(lattice[2][1]), float(lattice[2][2])]])
        for i in range(len(coordinate)):
            tmp_coor[0, 0] = float(coordinate[i][0])
            tmp_coor[1, 0] = float(coordinate[i][1])
            tmp_coor[2, 0] = float(coordinate[i][2])
            cart = np.dot(tmp_lattice.T, tmp_coor)
            coor = [str(cart[0, 0]), str(cart[1, 0]), str(cart[2, 0])]
            coor_coonverted.append(coor)
        return coor_coonverted

# read vasp_run.xml
with open("vasprun.xml", "r") as f:
    line = f.readlines()
lattice = []
coordinate = []
stress = []
forces = []
energy = []
atom_type = []
atom_num = []

# extract elements
flag = 0
for i in range(len(line)):
    if re.search("<set>", line[i]):
        flag = 1
        continue
    if re.search("</set>", line[i]):
        flag = 0
        break
    if flag == 1:
        tmp = line[i].split()[0]
        tmp = tmp.replace("<rc><c>", "")
        tmp = tmp.replace("</c><c>", "")
        atom_type.append(tmp)

for i in range(len(line)):
    tmp =  []
    if re.search("name=\"basis\"", line[i]):
        counter_b += 1
        if counter_b%freq == 0:
            l_x = line[i+1].split()
            l_y = line[i+2].split()
            l_z = line[i+3].split()
            lattice.append([[l_x[1], l_x[2], l_x[3]], [l_y[1], l_y[2], l_y[3]], [l_z[1], l_z[2], l_z[3]]])
            #if re.search("name=\"e_fr_energy\"", line[i-7]):
                # counter_e += 1
                # if counter_e%freq == 0:
            energy.append(line[i-7].split()[2])
    if re.search("name=\"positions\"", line[i]):
        counter_p += 1
        if counter_p%freq == 0:
            for j in range(len(atom_type)):
                tmp.append(line[i+j+1].split()[1:-1])
            coordinate.append(tmp)
    if re.search("name=\"stress\"", line[i]):
        counter_s += 1
        if counter_s%freq == 0:
            s_x = line[i+1].split()
            s_y = line[i+2].split()
            s_z = line[i+3].split()
            stress.append([[s_x[1], s_x[2], s_x[3]], [s_y[1], s_y[2], s_y[3]], [s_z[1], s_z[2], s_z[3]]])
    if re.search("name=\"forces\"", line[i]):
        counter_f += 1
        if counter_f%freq == 0:
            for j in range(len(atom_type)):
                tmp.append(line[i+j+1].split()[1:-1])
            forces.append(tmp)

if freq == 1:
    lattice = lattice[2:]
    coordinate = coordinate[2:]
    energy = energy[2:]
    stress = stress[2:]
elif freq == 2:
    lattice = lattice[1:]
    coordinate = coordinate[1:]
    energy = energy[1:]
    stress = stress[1:]
else:
    lattice = lattice[0:]
    coordinate = coordinate[0:]
    energy = energy[0:]
    stress = stress[0:]


for i in range(len(lattice)):
    coordinate[i] = convert_coor(lattice[i], coordinate[i], 0)


with open("train"+ str(len(energy)) +".xyz", "w") as f:
    for i in range(len(energy)):
        f.write(str(len(atom_type)) + "\n")
        f.write("Lattice=\"" + lattice[i][0][0] + " " + lattice[i][0][1] + " " + lattice[i][0][2] + " " + lattice[i][1][0] + " " + lattice[i][1][1] + " " + lattice[i][1][2] + " " + lattice[i][2][0] + " " + lattice[i][2][1] + " " + lattice[i][2][2] + "\" ")
        f.write("Properties=species:S:1:pos:R:3:forces:R:3 ")
        f.write("energy=" + energy[i] + " ")
        f.write("stress=\"" + stress[i][0][0] + " " + stress[i][0][1] + " " + stress[i][0][2] + " " + stress[i][1][0] + " " + stress[i][1][1] + " " + stress[i][1][2] + " " + stress[i][2][0] + " " + stress[i][2][1] + " " + stress[i][2][2] + "\" ")
        f.write("free_energy=" + energy[i] + " ")
        f.write("pbc=\"T T T\"\n")

        for j in range(len(atom_type)):
            f.write(atom_type[j] + "\t")
            f.write(coordinate[i][j][0] + "\t" + coordinate[i][j][1] + "\t" + coordinate[i][j][2] + "\t")
            f.write(forces[i][j][0] + "\t" + forces[i][j][1] + "\t" + forces[i][j][2] + "\n")




from genericpath import isfile
import os
import re
import shutil
import argparse
import random

# POSCAR is Direct & Selectie dynamics

path_vasp = "/home/thermal/VASP/vasp.6.4.0/bin/vasp_std"
mpi_num = "16"
initv = -0.075   # unit : Angs. / fs
x_pos = 0.0
y_pos = 0.0
z_pos = 0.6
with open("POSCAR", "r") as f:
    lines = f.readlines()
    shot_atom = lines[5].split()[1]


parser = argparse.ArgumentParser(description="input two argument")
parser.add_argument("-d", required=True, help="Please input directory name")
parser.add_argument("-n", required=True, type=int, help="Please input the number of executions")
args = parser.parse_args()

path = os.getcwd()
dirlist = os.listdir(path)
dir_list = []
for i in dirlist:
    if os.path.isdir(i):
        dir_list.append(i)
while True:
    flag = 0
    for i in dir_list:
        if re.search(args.d, i):
            print("The directory named {} already exists".format(args.d))
            flag = 1
            break
    if flag == 1:
        exit()
    else:
        break


for calc_num in range(int(args.n)):
    dir_name = args.d + "_" +str(calc_num + 1)
    os.makedirs(dir_name)
    
    if calc_num == 0:
        shutil.copy("INCAR", dir_name)
        if os.path.isfile("POSCAR"):
            shutil.copy("POSCAR", dir_name)
        elif os.path.isfile("CONTCAR"):
            shutil.copy("CONTCAR", dir_name + "/POSCAR")
        shutil.copy("KPOINTS", dir_name)
        if os.path.isfile("ML_AB"):
            shutil.copy("ML_AB", dir_name + "/ML_AB")
        if os.path.isfile("ML_ABN"):
            shutil.copy("ML_ABN", dir_name + "/ML_AB")
        if os.path.isfile("ML_FF"):
            shutil.copy("ML_FF", dir_name + "/ML_FF")
        if os.path.isfile("ML_FFN"):
            shutil.copy("ML_FFN", dir_name + "/ML_FF")
        shutil.copy("ICONST", dir_name + "/ICONST")
        shutil.copy("POTCAR", dir_name + "/POTCAR")
        
        os.chdir(dir_name)        
        os.system("mpirun -np " + mpi_num + " " + path_vasp)
        os.chdir("..")
        
    else:
        dir_name_b = args.d + "_" +  str(calc_num)
        f = open(dir_name_b + "/INCAR", "r")
        line = f.readlines()
        for i in line:
            if re.search("NSW", i):
                tmp = i.split()
                nsw = tmp[2]
        f = open(dir_name_b + "/OSZICAR", "r")
        line = f.readlines()
        count = 0
        for i in line:
            if re.search("T=", i):
                count += 1
        if count != int(nsw):
            print("Stop Calculation")
            exit()
        
        #rewrite POSCAR
        shutil.copy(dir_name_b + "/CONTCAR", dir_name + "/POSCAR")
        with open(dir_name + "/POSCAR", "r") as f:
            lines = f.readlines()
            atom_num = lines[6].split()
            atom_total = 0
            for i in range(len(atom_num)):
                atom_total = atom_total + int(atom_num[i])
            atom_num[1] = str(int(atom_num[1]) + 1)
            print(atom_total)

            # add atom
            newpos = []
            for i in range(9+atom_total):
                newpos.append(lines[i])

            x_pos = random.random()
            y_pos = random.random()

            new_atom_pos = str(x_pos) + " " + str(y_pos) + " " + str(z_pos) + " T T T\n"
            newpos.append(new_atom_pos)

            newpos[6] = atom_num[0] + " " + atom_num[1] + "\n"
        
            new_velocity = []
            for i in range(atom_total+1):
                if i == int(atom_total):
                    new_velocity.append("0 0 " + str(initv) + "\n")
                else:
                    new_velocity.append("0 0 0\n")
            print(new_velocity)
        with open(dir_name + "/POSCAR", "w") as f:
            for i in range(len(newpos)):
                print(newpos[i], file=f, end="")
            print("", file=f)
            for i in range(len(new_velocity)):
                print(new_velocity[i], file=f, end="")

        shutil.copy(dir_name_b + "/INCAR", dir_name)
        shutil.copy(dir_name_b + "/KPOINTS", dir_name)
        shutil.copy(dir_name_b + "/POTCAR", dir_name)
        if os.path.isfile(dir_name_b + "/ML_FF"):
            shutil.copy(dir_name_b + "/ML_FF", dir_name + "/ML_FF")
        if os.path.isfile(dir_name_b + "/ML_ABN"):
            shutil.copy(dir_name_b + "/ML_ABN", dir_name + "/ML_AB")
        shutil.copy(dir_name_b + "/ICONST", dir_name + "/ICONST")
        
        os.chdir(dir_name)
        os.system("mpirun -np " + mpi_num + " " + path_vasp)
        os.chdir("..")
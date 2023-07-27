from genericpath import isfile
import os
import re
import shutil
import argparse

path_vasp = "/home/owner/VASP/vasp.6.4.0/bin/vasp_std"
mpi_num = "32"

parser = argparse.ArgumentParser(description="input two argument")
parser.add_argument("-d", required=True, help="Please input directory name")
parser.add_argument("-n", required=True, type=int, help="Please input the number of executions")
args = parser.parse_args()

path = os.getcwd()
dirlist = os.listdir(path)
dir_list = []
ctifor_list = []
cti_flag = False

with open("INCAR", "r") as f:
    line = f.readlines()
    for i in line:
        if re.search("NSW", i):
                tmp = i.split()
                nsw = tmp[2]
        if re.search("ML_CTIFOR", i):
            cti_flag = True

if cti_flag == False:
    with open("INCAR", "a") as f:
        if re.search("\n", line[-1]):
            print("ML_CTIFOR = 0.002", file=f)

        else:
            print("\nML_CTIFOR = 0.002", file = f)



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
        shutil.copy("POTCAR", dir_name)
        if os.path.isfile("ML_ABN"):
            shutil.copy("ML_ABN", dir_name + "/ML_AB")
        shutil.copy("ICONST", dir_name + "/ICONST")
        
        os.chdir(dir_name)        
        os.system("mpirun -np " + mpi_num + " " + path_vasp)

        # get new ML_CTIFOR value
        if os.path.isfile("ML_LOGFILE"):
            with open("ML_LOGFILE", "r") as f:
                line = f.readlines()
                for i in range(len(line)):
                    if re.search("BEEF", line[i]):
                        beef_list = line[i].split()
                        if beef_list[1] == nsw:
                            *_, ctifor, _, _ = line[i].split()


        os.chdir("..")
        
    else:
        dir_name_b = args.d + "_" +  str(calc_num)
        f = open(dir_name_b + "/OSZICAR", "r")
        line = f.readlines()
        count = 0
        for i in line:
            if re.search("T=", i):
                count += 1
        if count != int(nsw):
            print("Stop Calculation")
            exit()
        
        shutil.copy(dir_name_b + "/INCAR", dir_name)
        shutil.copy(dir_name_b + "/CONTCAR", dir_name + "/POSCAR")
        shutil.copy(dir_name_b + "/KPOINTS", dir_name)
        shutil.copy(dir_name_b + "/POTCAR", dir_name)
        shutil.copy(dir_name_b + "/ML_ABN", dir_name + "/ML_AB")
        shutil.copy(dir_name_b + "/ICONST", dir_name + "/ICONST")
        
        os.chdir(dir_name)
        #change ML_CTIFOR
        with open("INCAR", "r") as f:
            line = f.readlines()
            for i in range(len(line)):       
                if re.search("ML_CTIFOR", line[i]):
                    line[i] = "ML_CTIFOR = " + ctifor + "\n"
        with open("INCAR", "w") as f:
            for i in line:
                print(i, end = "", file = f)

        os.system("mpirun -np " + mpi_num + " " + path_vasp)
        ctifor_list.clear() # initialize
        # get new ML_CTIFOR value
        if os.path.isfile("ML_LOGFILE"):
            with open("ML_LOGFILE", "r") as f:
                line = f.readlines()
                for i in range(len(line)):
                    if re.search("BEEF", line[i]):
                        if line[i].split()[1] == nsw:
                            *_, ctifor, _, _ = line[i].split()

        os.chdir("..")
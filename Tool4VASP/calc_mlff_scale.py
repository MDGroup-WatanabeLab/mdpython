from genericpath import isfile
import os
import re
import shutil
import argparse

# program execute : $ nohup python calc_mlff_scale_6.35 -d [name of directories before number] &

# change in case of PC or number of parallel
path_vasp = "/home/owner/VASP/vasp.6.4.0/bin/vasp_std"
mpi_num = "16"

# scaling factor for 2nd line in POSCAR
start = 0.9
end = 1.1
step = 0.05 
scaler = [float(x/100) for x in range(int(start * 100), int(end * 100) + 1, int(step * 100))]
dir_num = 0


parser = argparse.ArgumentParser(description="input two argument")
parser.add_argument("-d", required=True, help="Please input directory name")
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


for calc_num in scaler:
    dir_num+=1
    dir_name = args.d + "_" +"{:.02f}".format(calc_num)+"_"+str(dir_num)
    os.makedirs(dir_name)
    
    if dir_num == 1:
        shutil.copy("INCAR", dir_name)
        if os.path.isfile("POSCAR"):
            shutil.copy("POSCAR", dir_name)
        elif os.path.isfile("CONTCAR"):
            shutil.copy("CONTCAR", dir_name + "/POSCAR")
        shutil.copy("KPOINTS", dir_name)
        shutil.copy("POTCAR", dir_name)
        if os.path.isfile("ML_ABN"):
            shutil.copy("ML_ABN", dir_name + "/ML_AB")
        if os.path.isfile("ML_FF"):
            shutil.copy("ML_FF", dir_name + "/ML_FF")
        shutil.copy("ICONST", dir_name + "/ICONST")
        
        os.chdir(dir_name) 
        with open("POSCAR", "r") as f:
            line = f.readlines()
            line[1] = str(calc_num) + "\n"
        with open("POSCAR", "w") as f:
            f.writelines(line)       
        os.system("mpirun -np " + mpi_num + " " + path_vasp)
        os.chdir("..")
        
    else:
        # dir_name_b = args.d + "_" +  str(float((int(100*calc_num)-int(100*step))/100)) +"_"+str(dir_num-1)
        dir_name_b = args.d + "_" +  "{:.02f}".format(scaler[dir_num-2]) +"_"+str(dir_num-1)
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
        #if count != int(nsw):
            #print("Stop Calculation")
            #exit()
        
        # copy from previous directory
        shutil.copy(dir_name_b + "/INCAR", dir_name)
        
        # reset structure each calculation
        shutil.copy("POSCAR", dir_name + "/POSCAR") 
        # continue to use same structure
        # shutil.copy(dir_name_b + "POSCAR", dir_name + "/POSCAR")

        shutil.copy(dir_name_b + "/KPOINTS", dir_name)
        shutil.copy(dir_name_b + "/POTCAR", dir_name)
        if os.path.isfile(dir_name_b + "/ML_ABN"):
            shutil.copy(dir_name_b + "/ML_ABN", dir_name + "/ML_AB")
        if os.path.isfile(dir_name_b + "/ML_FF"):
            shutil.copy(dir_name_b + "/ML_FF", dir_name + "/ML_FF")
        shutil.copy(dir_name_b + "/ICONST", dir_name + "/ICONST")
        
        os.chdir(dir_name)
        with open("POSCAR", "r") as f:
            line = f.readlines()
            line[1] = str(calc_num) + "\n"
        with open("POSCAR", "w") as f:
            f.writelines(line)
        os.system("mpirun -np " + mpi_num + " " + path_vasp)
        os.chdir("..")



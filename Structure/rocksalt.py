# GST(Ge2Sb2Te5), NaCl, MgO and CaO of rocksalt structure
import os
import math
import numpy as np
import random

# select Atom
atomflag = int(input("Select atoms from following: \n"
                     "0 : GST \n"
                     "1 : NaCl \n"
                     "2 : MgO \n"
                     "3 : CaO \n"
                     "4 : GeTe with vacancy (1/10)\n"
                     "5 : SbTe with vacancy for Sb:Te=2:3\n"
                     "6 : GeSb with vacancy (1/10)\n"
                     "7 : GeTe\n"
                     "8 : SbTe\n"
                     "9 : GeSb\n"
                     "Input number : "))

# input lattice size
while True:
    print(
        "If you make GST, it is necessary to include one multiple of 5 at least\n"
        "If you make SbTe, it is necessary to include one multiple of 3 at least\n"
        )
    size = input("Please input the lattice size [ x, y, z ] : ").split()
    
    if len(size) == 3:
        for i in range(len(size)):
            if str(size[i]).isdecimal() and int(size[i]) > 0:
                flag = 1
            else:
                flag = 0
                break
    if flag == 1:
        break


# lattice parameter of unit cell
if atomflag == 0:
    l_a = 5.1249
    l_b = 5.1249
    l_c = 5.1249

elif atomflag == 1: # NaCl
    l_a = 5.640
    l_b = 5.640
    l_c = 5.640

elif atomflag == 1: # MgO
    l_a = 4.2113
    l_b = 4.2113
    l_c = 4.2113

elif atomflag == 2: # CaO
    l_a = 4.8152
    l_b = 4.8152
    l_c = 4.8152

elif atomflag == 4 or atomflag == 7: # GeTe, mp-2612
    l_a = 6.01
    l_b = 6.01
    l_c = 6.01

elif atomflag == 5 or atomflag == 8: #SbTe, mp-7716
    l_a = 6.34
    l_b = 6.34
    l_c = 6.34

elif atomflag == 6 or atomflag == 9: #GeSb, mp-9935
    l_a = 5.83
    l_b = 5.83
    l_c = 5.83


# wycoff position of plus ion, 4a
x_pls = 0.0
y_pls = 0.0
z_pls = 0.0
wyckoff_pls = [[0.0, 0.0, 0.0], [1/2, 0.0, 1/2], [0.0, 1/2, 1/2], [1/2, 1/2, 0.0]]
for i in range(len(wyckoff_pls)):
    for j in range(3):
        if wyckoff_pls[i][j] < 0:
            wyckoff_pls[i][j] = 1 + wyckoff_pls[i][j]

# wycoff position of minus ion, 4b
x_o = 1/2
y_o = 1/2
z_o = 1/2
wyckoff_mns = [[x_o, y_o, z_o], [x_o, 0, 0], [0, y_o, 0], [0, 0, z_o]]
for j in range(3):
    if wyckoff_mns[i][j] < 0:
        wyckoff_mns[i][j] = 1 + wyckoff_mns[i][j]

# lattice parameter (matrix format)
l_rocksalt = np.array([[l_a * float(size[0]), 0, 0], 
                    [0, l_b * float(size[1]), 0], 
                    [0, 0, l_c * float(size[2])]])

# coordinate list
position_pls = []
position_mns = []
position_ge = []
position_sb = []
position_te = []

# position of plus ion : Na, Mg, Ca or Te
if atomflag == 4 or atomflag == 6: #GeTe
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_pls)):
                    temp = np.zeros(shape=(3, 1)) 
                    temp[0, 0] = (wyckoff_pls[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_pls[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_pls[l][2] + k)/float(size[2]) 
                    pls = np.dot(l_rocksalt.T, temp) 
                    
                    if pls[0, 0] >= 0 and pls[0, 0] <= l_rocksalt[0, 0]: 
                        position_pls.append("{} {} {}".format(pls[0, 0], pls[1, 0], pls[2, 0]))

    np.random.shuffle(position_pls) # shuffle because Ge and Sb exist in random position
    length = float(len(position_pls)) * 9/10
    tp = random.sample(position_pls, int(length)) # pick up Ge and Sb position

    for i in range(len(tp)): # make Ge and Sb position
            position_te.append(tp[i])

else: 
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_pls)):
                    temp = np.zeros(shape=(3, 1)) 
                    temp[0, 0] = (wyckoff_pls[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_pls[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_pls[l][2] + k)/float(size[2]) 
                    pls = np.dot(l_rocksalt.T, temp) 
                    
                    if pls[0, 0] >= 0 and pls[0, 0] <= l_rocksalt[0, 0]: 
                        position_pls.append("{} {} {}".format(pls[0, 0], pls[1, 0], pls[2, 0]))

# position of minus ion
if atomflag != 0 and atomflag != 4 and atomflag != 5 and atomflag != 6: # except for GST, NaCl, MgO or CaO
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_mns)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_mns[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_mns[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_mns[l][2] + k)/float(size[2])
                    mns = np.dot(l_rocksalt.T, temp)
                    
                    if mns[0, 0] >= 0 and mns[0, 0] <= l_rocksalt[0, 0]:
                        position_mns.append("{} {} {}".format(mns[0, 0], mns[1, 0], mns[2, 0]))

elif atomflag == 0: # GST
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_mns)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_mns[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_mns[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_mns[l][2] + k)/float(size[2])
                    mns = np.dot(l_rocksalt.T, temp)

                    if mns[0, 0] >= 0 and mns[0, 0] <= l_rocksalt[0, 0]:
                        position_mns.append("{} {} {}".format(mns[0, 0], mns[1, 0], mns[2, 0]))


    np.random.shuffle(position_mns) # shuffle because Ge and Sb exist in random position
    length = float(len(position_mns)) * 4/5
    g_s = random.sample(position_mns, int(length)) # pick up Ge and Sb position

    for i in range(len(g_s)): # make Ge and Sb position
        if i < len(g_s) / 2:
            position_ge.append(g_s[i])
        elif i >= len(g_s) / 2:
            position_sb.append(g_s[i])

elif atomflag == 4 or atomflag == 6: #GeTe, GeSb
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_mns)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_mns[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_mns[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_mns[l][2] + k)/float(size[2])
                    mns = np.dot(l_rocksalt.T, temp)

                    if mns[0, 0] >= 0 and mns[0, 0] <= l_rocksalt[0, 0]:
                        position_mns.append("{} {} {}".format(mns[0, 0], mns[1, 0], mns[2, 0]))

    np.random.shuffle(position_mns) # shuffle because Ge and Sb exist in random position
    length = float(len(position_mns)) * 9/10
    g_s = random.sample(position_mns, int(length)) # pick up Ge and Sb position
    for i in range(len(g_s)): # make Ge and Sb position    
        position_ge.append(g_s[i])

elif atomflag == 5: #SbTe
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            for k in range(int(size[2])):
                for l in range(len(wyckoff_mns)):
                    temp = np.zeros(shape=(3, 1))
                    temp[0, 0] = (wyckoff_mns[l][0] + i)/float(size[0])
                    temp[1, 0] = (wyckoff_mns[l][1] + j)/float(size[1])
                    temp[2, 0] = (wyckoff_mns[l][2] + k)/float(size[2])
                    mns = np.dot(l_rocksalt.T, temp)

                    if mns[0, 0] >= 0 and mns[0, 0] <= l_rocksalt[0, 0]:
                        position_mns.append("{} {} {}".format(mns[0, 0], mns[1, 0], mns[2, 0]))

    np.random.shuffle(position_mns) # shuffle because Ge and Sb exist in random position
    length = float(len(position_mns)) * 2/3
    sbp = random.sample(position_mns, int(length)) # pick up Ge and Sb position
    for i in range(len(sbp)): # make Ge and Sb position    
        position_sb.append(sbp[i])


# write POSCAR
file = "POSCAR"
if os.path.exists(file):
    os.remove(file)
f = open(file, "w")
f.write("rocksalt_{}x{}x{}\n".format(size[0], size[1], size[2]))
f.write("1.0\n")
for i in range(3):
    for j in range(3):
        f.write("{} ".format(l_rocksalt[i][j]))
    f.write("\n")


if atomflag == 1: # NaCl
    f.write("Na Cl\n")
elif atomflag == 2: # MgO
    f.write("Mg O\n")
elif atomflag == 3: # CaO
    f.write("Ca O\n")
elif atomflag == 4 or atomflag == 7: # GeTe with vacancy and no vacancy
    f.write("Te Ge\n")
elif atomflag == 5 or atomflag == 8: # SbTe with vacancy and no vacancy
    f.write("Te Sb\n")
elif atomflag == 6 or atomflag == 9: # GeSb with vacancy and no vacancy
    f.write("Ge Sb\n")
elif atomflag == 0: # GST
    f.write("Te Ge Sb\n")


if atomflag == 0: # GST
    f.write("{} {} {}\n".format(len(position_pls), len(position_ge), len(position_sb)))
elif atomflag == 4 or atomflag == 6: #GeTe
    f.write("{} {}\n".format(len(position_te), len(position_ge)))
elif atomflag == 5: #SbTe
    f.write("{} {}\n".format(len(position_pls), len(position_sb)))
else:  # Except GST
    f.write("{} {}\n".format(len(position_pls), len(position_mns)))

f.write("Cartesian\n")
if atomflag == 0: # GST
    for i in position_pls: # Te
        f.write(i + "\n")
    for i in position_ge:  # Ge
        f.write(i + "\n")
    for i in position_sb:  # Sb
        f.write(i + "\n")
elif atomflag == 4 or atomflag == 6: # GeTe, GeSb
    for i in position_te:
        f.write(i + "\n")
    for i in position_ge:
        f.write(i + "\n")
elif atomflag == 5: # SbTe
    for i in position_pls:
        f.write(i + "\n")
    for i in position_sb:
        f.write(i + "\n")
else: # Except GST
    for i in position_pls:
        f.write(i + "\n")
    for i in position_mns:
        f.write(i + "\n")

f.close()
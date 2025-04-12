# this program can be used for lectangier (α=β=γ=90°)
# "range" decides range of not moving
range_z = 0.25

# read POSCAR
with open("CONTCAR", "r") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")

flag_cartesian = True
if lines[7] == "Direct":
    flag_cartesian = False


# insert "Selectie dynamics"
lines.insert(7, "Selective dynamics")

# separate lattice & position
lattice_para = lines[0:9]
position = lines[9:]

for i in range(len(position)):
    position[i] = position[i].split()


# get z position and z length
position_z = []
for i in range(len(position)):
    position_z.append(float(position[i][2]))
zmax = max(position_z)
zmin = min(position_z)
zlength = zmax-zmin

# set capability (TTT or FFF)
move = []
if flag_cartesian:
    for i in range(len(position)):
        if position_z[i] <= zlength*range_z+zmin:
            move.append("F F F") # don't move
        if position_z[i] > zlength*range_z+zmin:
            move.append("T T T") # can move

else:
     for i in range(len(position)):
        if position_z[i] <= range_z+zmin/zlength:
            move.append("F F F") # don't move
        if position_z[i] > range_z+zmin/zlength:
            move.append("T T T") # can move   

# write POSCAR_selected
with open("CONTCAR_selected", "w") as f:
    for i in range(len(lattice_para)):
        f.write(lattice_para[i]+"\n")
    for i in range(len(position)):
        for j in range(3):
            f.write("{:.6f}\t".format(float(position[i][j])))
        f.write(move[i]+"\n")

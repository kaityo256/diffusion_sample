import re


def read_position(f):
    n = 0
    line = f.readline()
    qx = []
    qy = []
    qz = []
    while line:
        if re.compile("ITEM: TIMESTEP").search(line):
            print(qx)
            exit()
            return
        a = line.split()
        qx.append(float(a[2]))
        qy.append(float(a[2]))
        qz.append(float(a[2]))
        n += 1
        line = f.readline()


time = 0
with open("diffusion.lammpstrj") as f:
    line = f.readline()
    while line:
        if re.compile("ITEM: TIMESTEP").search(line):
            time += 1
            print(time)
        elif re.compile("ITEM: ATOMS").search(line):
            read_position(f)
        line = f.readline()

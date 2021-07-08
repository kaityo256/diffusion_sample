import re

time = 0
with open("diffusion.dump") as f:
    line = f.readline()
    while line:
        if re.compile("ITEM: TIMESTEP").search(line):
            time += 1
            print(time)
        line = f.readline()

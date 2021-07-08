import re
import numpy as np

L = 20           # システムサイズ
N = (L//2)**3*4  # 原子数
dt = 0.001       # 時間刻み


def read_position(f):
    n = 0
    line = f.readline()
    qx = np.zeros(N)
    qy = np.zeros(N)
    qz = np.zeros(N)
    while line:
        if re.compile("ITEM: TIMESTEP").search(line):
            return qx, qy, qz
        a = line.split()
        i = int(a[0])-1
        qx[i] = float(a[2])*L
        qy[i] = float(a[3])*L
        qz[i] = float(a[4])*L
        line = f.readline()
    return [], [], []


pos = []
x = []
y = []
z = []
with open("diffusion.lammpstrj") as f:
    line = f.readline()
    while line:
        if re.compile("ITEM: ATOMS").search(line):
            qx, qy, qz = read_position(f)
            if len(qx):
                x.append(qx)
                y.append(qy)
                z.append(qz)
        line = f.readline()

# トータルタイムステップ
time = len(x)

# 周期境界条件補正
# システムボックスをまたぐと急に距離が増えたように見えてしまうのを防ぐ
for i in range(N):
    for t in range(time-1):
        if x[t+1][i] - x[t][i] > L/2:
            x[t+1][i] -= L
        if y[t+1][i] - y[t][i] > L/2:
            y[t+1][i] -= L
        if z[t+1][i] - z[t][i] > L/2:
            z[t+1][i] -= L
        if x[t+1][i] - x[t][i] < -L/2:
            x[t+1][i] += L
        if y[t+1][i] - y[t][i] < -L/2:
            y[t+1][i] += L
        if z[t+1][i] - z[t][i] < -L/2:
            z[t+1][i] += L

# 拡散係数の計算

for t in range(time-1):
    r2 = 0.0
    for i in range(N):
        dx = x[t][i] - x[0][i]
        dy = y[t][i] - y[0][i]
        dz = z[t][i] - z[0][i]
        r2 += dx**2 + dy**2 + dz**2
    r2 = r2/N
    print(f"{t*dt} {r2}")

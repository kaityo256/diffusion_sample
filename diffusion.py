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
        # 次のフレームの最初の行が出てきたら読み込み終了
        if re.compile("ITEM: TIMESTEP").search(line):
            return qx, qy, qz
        a = line.split()
        i = int(a[0])-1         # 粒子番号
        qx[i] = float(a[2])*L   # x座標
        qy[i] = float(a[3])*L   # y座標
        qz[i] = float(a[4])*L   # z座標
        line = f.readline()
    return [], [], []


def read_file(filename):
    x = []
    y = []
    z = []
    with open(filename) as f:
        line = f.readline()
        while line:
            if re.compile("ITEM: ATOMS").search(line):
                qx, qy, qz = read_position(f)
                if len(qx):
                    x.append(qx)
                    y.append(qy)
                    z.append(qz)
            line = f.readline()
    return x, y, z


def adjust_periodic(x, y, z):
    """
    周期境界条件補正
    システムボックスをまたぐと急に距離が増えたように見えてしまうのを防ぐ
    時刻tと時刻t+1の座標を比較し、急激な変化がおきていたら修正
    """
    time = len(x)
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


def save_diffusion(x, y, z):
    """
    平均自乗変位の計算
    時刻t=0と、時刻tの距離の差の自乗を時間の関数としてプロット
    """
    with open("diffusion.dat", "w") as f:
        for t in range(len(x)-1):
            r2 = 0.0
            for i in range(N):
                dx = x[t][i] - x[0][i]
                dy = y[t][i] - y[0][i]
                dz = z[t][i] - z[0][i]
                r2 += dx**2 + dy**2 + dz**2
            r2 = r2/N
            f.write(f"{t*dt} {r2}\n")
    print("Generated diffusion.dat")


def save_trajectory(x, y, z):
    """
    0番の粒子の軌跡を表示する
    """
    with open("trajectory.dat", "w") as f:
        for t in range(len(x)):
            f.write(f"{x[t][0]} {y[t][0]} {z[t][0]}\n")
    print("Generated trajectory.dat")


if __name__ == '__main__':
    x, y, z = read_file("diffusion.lammpstrj")
    adjust_periodic(x, y, z)
    save_diffusion(x, y, z)
    save_trajectory(x, y, z)

import random
import numpy as np
from math import cos, sin, pi, sqrt

L = 20
N = (L//2)**3*4


def add_atom(qx, qy, qz, x, y, z):
    qx.append(x)
    qy.append(y)
    qz.append(z)


def makeconf():
    """
    初期状態を作る
    """
    qx = []
    qy = []
    qz = []
    px = []
    py = []
    pz = []
    # FCCに組む(密度0.5)
    h = 1.0
    for x in range(L//2):
        for y in range(L//2):
            for z in range(L//2):
                ix = x * 2
                iy = y * 2
                iz = z * 2
                add_atom(qx, qy, qz, ix, iy, iz)
                add_atom(qx, qy, qz, ix, iy+h, iz+h)
                add_atom(qx, qy, qz, ix+h, iy, iz+h)
                add_atom(qx, qy, qz, ix+h, iy+h, iz)
    # ランダムな向きに大きさ1の初速を与える
    v0 = 2.0
    for _ in range(N):
        phi = random.uniform(0, 2*pi)
        vz = random.uniform(-1, 1)
        vx = sqrt(1-vz**2)*cos(phi)
        vy = sqrt(1-vz**2)*sin(phi)
        px.append(v0*vx)
        py.append(v0*vy)
        pz.append(v0*vz)
    # 全体がドリフトしないように平均速度をゼロにする
    px = np.array(px)
    py = np.array(py)
    pz = np.array(pz)
    px -= np.average(px)
    py -= np.average(py)
    pz -= np.average(pz)
    return qx, qy, qz, px, py, pz


def save_file(filename, qx, qy, qz, px, py, pz):
    """
    配列からatomsファイルを作成する
    """
    with open(filename, "w") as f:
        f.write("Position Data\n\n")
        f.write(f"{N} atoms\n")
        f.write("1 atom types\n\n")
        f.write(f"0.0 {L} xlo xhi\n")
        f.write(f"0.0 {L} ylo yhi\n")
        f.write(f"0.0 {L} zlo zhi\n")
        f.write("\n")
        f.write("Atoms\n\n")
        for i in range(N):
            f.write(f"{i+1} 1 {qx[i]} {qy[i]} {qz[i]}\n")
        f.write("\n")
        f.write("Velocities\n\n")
        for i in range(N):
            f.write(f"{i+1} {px[i]} {py[i]} {pz[i]}\n")
    print("Generated {}".format(filename))


qx, qy, qz, px, py, pz = makeconf()

save_file("diffusion.atoms", qx, qy, qz, px, py, pz)

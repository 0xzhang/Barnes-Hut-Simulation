# Modified by 0xzhang.
import math
import taichi as ti
import numpy as np
from body import Body
from quadtree import Quad, QuadTree

ti.init(arch=ti.cpu)


# number of planets
N = 100
# init vel
init_vel = 120

# time-step size
h = 1e-4
# substepping
substepping = 10

# center of the screen
center = ti.Vector.field(2, ti.f32, ())
center[None] = [0.5, 0.5]

# pos, vel and force of the planets
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)

bodies = []

# init pos and vel
@ti.kernel
def ti_init():
    # galaxy size
    galaxy_size = 0.1
    # init vel
    init_vel = 120
    for i in range(N):
        theta = ti.random() * 2 * math.pi
        r = (ti.sqrt(ti.random()) * 0.6 + 0.4) * galaxy_size
        offset = r * ti.Vector([ti.cos(theta), ti.sin(theta)])
        pos[i] = center[None] + offset
        vel[i] = [-offset.y, offset.x]
        vel[i] *= init_vel

# init bodies list
def init():
    ti_init()
    p = pos.to_numpy()
    v = vel.to_numpy()
    for i in range(N):
        bodies.append(Body(1, p[i], v[i]))


def compute_force(tree):
    for body in bodies:
        body.reset_force()
        tree.apply_force(body)


def update():
    dt = h / substepping
    for body in bodies:
        body.update(dt)
    

def build_tree():
    qt = QuadTree(Quad(np.array([0.0, 0.0]), 1.0))
    for body in bodies:
        qt.insert(body)
    return qt

def step():
    qt = build_tree()
    for i in range(substepping):
        compute_force(qt)
        update()
    return qt

def display(gui):
    for body in bodies:
        body.display(gui)
    gui.show()

def main():
    gui = ti.GUI('N-body naive simulation', (800, 800))
    init()
    qt = build_tree()

    pause = True
    while gui.running:
        for e in gui.get_events(ti.GUI.PRESS):
            if e.key in [ti.GUI.ESCAPE, ti.GUI.EXIT]:
                exit()
            elif e.key == 'r':
                init()
            elif e.key == ti.GUI.SPACE:
                pause = not pause

        if not pause:
            qt = step()
        qt.display(gui)

        display(gui)

if __name__ == "__main__":
    main()
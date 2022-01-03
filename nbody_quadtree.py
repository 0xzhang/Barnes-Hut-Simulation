# Modified by 0xzhang.
import math
import taichi as ti
import numpy as np
from quadtree import Quad, QuadTree

ti.init(arch=ti.cpu)

# gravitational constant 6.67408e-11, using 1 for simplicity
G = 1
# number of planets
N = 100
# unit mass
m = 1
# planet radius (for rendering)
planet_radius = 2
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
force = ti.Vector.field(2, ti.f32, N)


@ti.kernel
def init():
    # galaxy size
    galaxy_size = 0.2
    # init vel
    init_vel = 120
    for i in range(N):
        theta = ti.random() * 2 * math.pi
        r = (ti.sqrt(ti.random()) * 0.6 + 0.4) * galaxy_size
        offset = r * ti.Vector([ti.cos(theta), ti.sin(theta)])
        pos[i] = center[None] + offset
        vel[i] = [-offset.y, offset.x]
        vel[i] *= init_vel
    
@ti.kernel
def compute_force():
    # clear force
    for i in range(N):
        force[i].fill(0.0)
    # compute gravitational force
    for i in range(N):
        p = pos[i]
        for j in range(N):
            diff = p - pos[j]
            r = diff.norm(1e-5)
            # gravitational force -(GMm / r^2) * (diff/r) for i
            f = -G * m * m * (1.0 / r)**3 * diff
            # assign to each particle
            force[i] += f

@ti.kernel
def update():
    dt = h / substepping
    for i in range(N):
        # symplectic euler
        vel[i] += dt * force[i] / m
        pos[i] += dt * vel[i]
        
def step():
    for i in range(substepping):
        compute_force()
        update()

def build_tree(qt: QuadTree):
    for i in range(N):
        qt.insert(i, pos[i].to_numpy())

def main():
    gui = ti.GUI('N-body simulation with quadtree', (800, 800))
    init()

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
            step()

        qt = QuadTree(Quad(np.array([0.0, 0.0]), 1.0))
        build_tree(qt)
        qt.display(gui)

        gui.circles(pos.to_numpy(), color=0xffffff, radius=planet_radius)
        gui.show()

if __name__ == "__main__":
    main()

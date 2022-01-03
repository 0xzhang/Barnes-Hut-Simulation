# Modified by 0xzhang.
import math
import taichi as ti
import numpy as np
from body import Body

ti.init(arch=ti.cpu)

# number of planets
N = 100
# galaxy size
galaxy_size = 0.4

# time-step size
h = 1e-4
# substepping
substepping = 1
dt = h / substepping

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

def step():
    for i in range(substepping):
        for body in bodies:
            body.reset_force()
            for other in bodies:
                body.add_force(other)
        for body in bodies:
            body.update(dt)

def display(gui):
    for body in bodies:
        body.display(gui)
    gui.show()

def main():
    ui = True
    init()

    if ui:
        gui = ti.GUI('N-body naive simulation', (800, 800))
        pause = False
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

            display(gui)
    else:
        while True:
            step()

if __name__ == "__main__":
    main()

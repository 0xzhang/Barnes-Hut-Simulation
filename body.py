import numpy as np

# gravitational constant 6.67408e-11, using 1 for simplicity
G = 1

class Body:
    def __init__(self, mass, pos: np.ndarray, vel = np.zeros(2)):
        self.m = mass
        self.pos = pos
        self.vel = vel
        self.force = np.zeros(2)

    def reset_force(self):
        self.force = 0.0

    def add_force(self, body, eps = 1e-5):
        disp = self.pos - body.pos
        r = np.sqrt(disp.dot(disp) + eps**2)
        df = -G * self.m* body.m*disp/r**3
        self.force = self.force + df

    def update(self, dt):
        self.vel +=  dt * self.force / self.m
        self.pos += dt * self.vel

    def in_quad(self, quad):
        inX = self.pos[0] >= quad.ll[0] and self.pos[0] < quad.ur[0]
        inY = self.pos[1] >= quad.ll[1] and self.pos[1] < quad.ur[1]

        if inX and inY:
            return True
        else:
            return False

    def distance_to(self, body):
        disp = self.pos - body.pos
        return np.sqrt(disp.dot(disp))

    def display(self, gui):
        gui.circle(self.pos, color=0xffffff, radius=2)

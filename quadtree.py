import numpy as np
from body import Body


class Quad:

    def __init__(self, ll: np.ndarray, size: float):
        # lower left
        self.ll = ll
        # the length of the side of the cell
        self.size = size
        # upper right
        self.ur = self.ll + self.size
        # the center of the cell
        self.ccenter = self.ll + self.size / 2

    def SW(self):
        return Quad(self.ll, self.size / 2)

    def SE(self):
        return Quad(self.ll + [self.size / 2, 0.0], self.size / 2)

    def NW(self):
        return Quad(self.ll + [0.0, self.size / 2], self.size / 2)

    def NE(self):
        return Quad(self.ll + [self.size / 2, self.size / 2], self.size / 2)

    def display(self, gui):
        gui.rect(self.ll, self.ur, radius=1, color=0xED553B)
        # gui.rect(self.ll, self.ur, radius=self.size*3, color=0xED553B)


class QuadTree:

    def __init__(self, quad: Quad):
        self.quad = quad

    def insert(self, body: Body):
        if hasattr(self, 'body'):
            if self.external:
                # create 4 child trees
                self.SW = QuadTree(self.quad.SW())
                self.SE = QuadTree(self.quad.SE())
                self.NW = QuadTree(self.quad.NW())
                self.NE = QuadTree(self.quad.NE())
                if (self.body.in_quad(self.quad.SW())):
                    self.SW.insert(self.body)
                elif (self.body.in_quad(self.quad.SE())):
                    self.SE.insert(self.body)
                elif (self.body.in_quad(self.quad.NW())):
                    self.NW.insert(self.body)
                elif (self.body.in_quad(self.quad.NE())):
                    self.NE.insert(self.body)
                self.external = False
            # sort new body into child trees
            if body.in_quad(self.quad.SW()):
                self.SW.insert(body)
            elif body.in_quad(self.quad.SE()):
                self.SE.insert(body)
            elif body.in_quad(self.quad.NW()):
                self.NW.insert(body)
            elif body.in_quad(self.quad.NE()):
                self.NE.insert(body)
            # add to node body aggregate mass
            R, M = self.body.pos, self.body.m
            r, m = body.pos, body.m
            R = (M * R + m * r) / (M + m)
            M += m
            self.body = Body(M, R)
        else:
            # if node is empty, add body and make external node
            self.body = body
            self.external = True

    # evaluate force on body from tree with resolution theta
    def apply_force(self, body: Body, theta=1.0, eps=1e-5):
        # not an empty node
        if hasattr(self, 'body'):
            # distance of node body to body
            d = body.distance_to(self.body)
            if d != 0.0:
                # box sufficiently far away for its size, compute force
                if self.quad.size / d < theta or self.external:
                    body.add_force(self.body)
                else:
                    # box too close, compute forces from children instead
                    self.SW.apply_force(body, theta, eps)
                    self.SE.apply_force(body, theta, eps)
                    self.NW.apply_force(body, theta, eps)
                    self.NE.apply_force(body, theta, eps)

    def display(self, gui):
        if hasattr(self, 'body'):
            self.quad.display(gui)
            if not self.external:
                self.SW.display(gui)
                self.SE.display(gui)
                self.NW.display(gui)
                self.NE.display(gui)

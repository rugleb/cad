from time import time

import numpy as np
from scipy import optimize


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2


class Solver:
    def __init__(self):
        self.points = []

    def add_point(self, p: Point):
        self.points.append(p)

    def system(self, x: np.ndarray):
        y = np.zeros(x.shape, dtype=x.dtype)

        for i, p in enumerate(self.points):
            j = 2 * i
            y[j] = x[j] - p.x
            y[j + 1] = x[j + 1] - p.y

        return y

    @property
    def x0(self):
        size = len(self.points) * 2
        x0 = np.zeros(size, dtype=float)
        return x0

    def solve(self):
        result = optimize.fsolve(self.system, self.x0)
        return result


start = time()

solver = Solver()
solver.add_point(Point(10, 10))
solver.add_point(Point(10, 20))

res = solver.solve()

print(time() - start)
print(res)

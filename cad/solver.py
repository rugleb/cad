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

    def points(self) -> tuple:
        return self.p1, self.p2


class System:
    def __init__(self):
        self.points = []

    def add(self, point: Point):
        self.points.append(point)

    @property
    def x0(self) -> np.ndarray:
        size = len(self.points) * 2
        return np.ndarray(shape=(size, ), dtype=float)

    def system(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros(shape=x.shape, dtype=x.dtype)

        for i, point in enumerate(self.points):
            for j, prop in enumerate(['x', 'y']):
                n = i * 2 + j
                y[n] = x[n] - getattr(point, prop)

        return y

    def solve(self) -> list:
        result = []
        for y in optimize.fsolve(self.system, self.x0, xtol=1e-2):
            result.append(round(y, 2))
        return result

    def recount(self):
        y = self.solve()

        for i, point in enumerate(self.points):
            for j, prop in enumerate(['x', 'y']):
                n = i * 2 + j
                setattr(point, prop, y[n])


start = time()

system = System()
for value in range(5):
    system.add(Point(value, value))

solution = system.solve()
delta = time() - start

print(solution)
print(delta)

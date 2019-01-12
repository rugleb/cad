from time import time

import numpy as np
from scipy import optimize


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def coordinates(self) -> tuple:
        return self.x, self.y


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
            for j, coordinate in enumerate(point.coordinates):
                n = i * 2 + j
                y[n] = x[n] - coordinate

        return y

    def solve(self) -> list:
        result = []
        for y in optimize.fsolve(self.system, self.x0, xtol=1e-2):
            result.append(round(y, 2))
        return result

    def recount(self):
        y = self.solve()

        properties = ('x', 'y')
        for i, point in enumerate(self.points):
            for j, prop in enumerate(properties):
                n = i * 2 + j
                setattr(point, prop, y[n])


start = time()

p1 = Point(10., 10.)
p2 = Point(30., 10.)
p3 = Point(20., 20.)

system = System()
system.add(p1)
system.add(p2)
system.add(p3)

solution = system.solve()
delta = time() - start

print(solution)
print(delta)

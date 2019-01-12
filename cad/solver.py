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


class Constraint:
    pass


class Length(Constraint):
    def __init__(self, p1: Point, p2: Point, value: float):
        self.p1 = p1
        self.p2 = p2
        self.value = value


class System:
    def __init__(self):
        self.points = []
        self.constraints = []

    def add_point(self, point: Point):
        self.points.append(point)

    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

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


def main():
    p1 = Point(10., 10.)
    p2 = Point(30., 10.)
    p3 = Point(20., 20.)

    system = System()
    system.add_point(p1)
    system.add_point(p2)
    system.add_point(p3)

    length = Length(p1, p2, 20)
    system.add_constraint(length)

    return system.solve()


start = time()
solution = main()

delta = time() - start

print(solution)
print(delta)

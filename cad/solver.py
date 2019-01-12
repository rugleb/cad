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
        self.length = value

    def apply(self, system, x: np.ndarray, y: np.ndarray, i: int):
        i1 = system.points.index(self.p1) * 2
        i2 = system.points.index(self.p2) * 2

        y[i1 + 0] += 2 * x[i] * (x[i1 + 0] - x[i2 + 0])
        y[i1 + 1] += 2 * x[i] * (x[i1 + 1] - x[i2 + 1])

        y[i1 + 0] -= 2 * x[i] * (x[i1 + 0] - x[i2 + 0])
        y[i1 + 1] -= 2 * x[i] * (x[i1 + 1] - x[i2 + 1])

        y[i] = (x[i1] - x[i2]) ** 2 + (x[i1 + 1] - x[i2 + 1]) ** 2 - self.length ** 2


class FixedX(Constraint):
    def __init__(self, point: Point, value: float):
        self.point = point
        self.value = value

    def apply(self, system, x: np.ndarray, y: np.ndarray, i: int):
        j = system.points.index(self.point) * 2
        y[j] += x[i]

        y[i] = x[j] - self.value


class FixedY(Constraint):
    def __init__(self, point: Point, value: float):
        self.point = point
        self.value = value

    def apply(self, system, x: np.ndarray, y: np.ndarray, i: int):
        j = system.points.index(self.point) * 2 + 1
        y[j] += x[i]

        y[i] = x[j] - self.value


class Horizontal(Constraint):
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, system, x: np.ndarray, y: np.ndarray, i: int):
        i1 = system.points.index(self.p1) * 2 + 1
        i2 = system.points.index(self.p2) * 2 + 1

        y[i1] += x[i]
        y[i2] -= x[i]

        y[i] = x[i1] - x[i2]


class Vertical(Constraint):
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, system, x: np.ndarray, y: np.ndarray, i: int):
        i1 = system.points.index(self.p1) * 2
        i2 = system.points.index(self.p2) * 2

        y[i1] += x[i]
        y[i2] -= x[i]

        y[i] = x[i1] - x[i2]


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
        size = len(self.points) * 2 + len(self.constraints)
        y = np.zeros(shape=(size, ), dtype=float)

        for i, point in enumerate(self.points):
            for j, coordinate in enumerate(point.coordinates):
                n = i * 2 + j
                y[n] = coordinate

        for i, constraint in enumerate(self.constraints):
            n = len(self.points) * 2 + i
            y[n] = i + 1 + 1e-3

        return y

    def system(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros(shape=x.shape, dtype=x.dtype)

        for i, point in enumerate(self.points):
            for j, coordinate in enumerate(point.coordinates):
                n = i * 2 + j
                y[n] = 2 * (x[n] - coordinate)

        for i, constraint in enumerate(self.constraints):
            n = len(self.points) * 2 + i
            constraint.apply(self, x, y, n)

        return y

    def solve(self) -> list:
        result = []
        for y in optimize.fsolve(self.system, self.x0, xtol=1e-3):
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

    system = System()
    system.add_point(p1)
    system.add_point(p2)

    system.add_constraint(Length(p1, p2, 20.))
    system.add_constraint(FixedX(p2, p2.x))
    system.add_constraint(FixedY(p2, p2.y))

    return system.solve()


start = time()
solution = main()

delta = time() - start

print(solution)
print(delta)

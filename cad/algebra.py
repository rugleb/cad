from abc import abstractmethod

import numpy as np

from time import time
from typing import List
from scipy.optimize import fsolve, root
from PySide2.QtCore import QLineF, QPointF


Line = QLineF
Point = QPointF


ROUNDED = 2
INACCURACY = 2


def sqrt(x: float, rounded: int = ROUNDED) -> float:
    return np.round(np.sqrt(x), rounded)


def p2p(p1: Point, p2: Point, rounded: int = ROUNDED) -> float:
    dx = p2.x() - p1.x()
    dy = p2.y() - p1.y()
    return sqrt(dx ** 2 + dy ** 2, rounded)


def p2l(point: Point, line: Point, rounded: int = ROUNDED) -> float:
    if line.length() > 0:
        x0, y0 = point.x(), point.y()
        x1, y1 = line.x1(), line.y1()
        x2, y2 = line.x2(), line.y2()
        square = (y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1
        dist = abs(square) / line.length()
        return round(dist, rounded)
    else:
        return p2p(line.p1(), point)


def p2s(point: Point, line: Line, rounded: int = ROUNDED) -> float:
    dist = p2l(point, line, rounded)
    if 0. == dist:
        if line.x1() > line.x2():
            line = Line(line.p2(), line.p1())
        if line.x1() <= point.x() <= line.x2():
            return 0.
        if point.x() < line.x1():
            return p2p(point, line.p1())
        return p2p(point, line.p2())
    return dist


class Constraint(object):

    @abstractmethod
    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        pass


class Length(Constraint):

    def __init__(self, p1: Point, p2: Point, length: float):
        self.p1 = p1
        self.p2 = p2
        self.length = length

    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        i1 = solver.points.index(self.p1) * 2
        i2 = solver.points.index(self.p2) * 2

        dx = x[i2 + 0] - x[i1 + 0]
        dy = x[i2 + 1] - x[i1 + 1]

        y[i2] += 2 * x[n] * dx
        y[i1] -= 2 * x[n] * dx

        y[i2 + 1] += 2 * x[n] * dy
        y[i1 + 1] -= 2 * x[n] * dy

        y[n] = dx ** 2 + dy ** 2 - self.length ** 2


class Horizontal(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        i1 = solver.points.index(self.p1) * 2 + 1
        i2 = solver.points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class Vertical(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        i1 = solver.points.index(self.p1) * 2
        i2 = solver.points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class FixingX(Constraint):

    def __init__(self, point: Point, lock: float):
        self.point = point
        self.lock = lock

    def apply(self, solver, x: list, y: list, n: int):
        i = solver.points.index(self.point) * 2
        y[i] += x[n]
        y[n] = x[i] - self.lock


class FixingY(Constraint):

    def __init__(self, point: Point, lock: float):
        self.point = point
        self.lock = lock

    def apply(self, solver, x: list, y: list, n: int):
        i = solver.points.index(self.point) * 2 + 1
        y[i] += x[n]
        y[n] = x[i] - self.lock


class CoincidentX(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        i1 = solver.points.index(self.p1) * 2
        i2 = solver.points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class CoincidentY(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        i1 = solver.points.index(self.p1) * 2 + 1
        i2 = solver.points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class PerpendicularConstraint(Constraint):

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        pass


class Parallel(Constraint):

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def apply(self, solver, x: np.ndarray, y: np.ndarray, n: int):
        i1 = solver.points.index(self.p1) * 2
        i2 = solver.points.index(self.p2) * 2
        i3 = solver.points.index(self.p3) * 2
        i4 = solver.points.index(self.p4) * 2

        ax = x[i2] - x[i1]
        bx = x[i4] - x[i3]
        ay = x[i2 + 1] - x[i1 + 1]
        by = x[i4 + 1] - x[i3 + 1]

        y[i1] -= by * x[n]
        y[i2] += by * x[n]
        y[i3] += ay * x[n]
        y[i4] -= ay * x[n]

        y[i1 + 1] += bx * x[n]
        y[i2 + 1] -= bx * x[n]
        y[i3 + 1] -= ax * x[n]
        y[i4 + 1] += ax * x[n]

        y[n] = ax * by - ay * bx


class AngleConstraint(Constraint):

    def __init__(self, line: Line, angle: float):
        self.line = line
        self.angle = angle


Points = List[Point]
Constraints = List[Constraint]


class Solver(object):

    def __init__(self):
        self.points: Points = []
        self.constraints: Constraints = []

    def system(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros(x.shape, x.dtype)

        for i, point in enumerate(self.points):
            y[i * 2 + 0] = 2 * (x[i * 2 + 0] - point.x())
            y[i * 2 + 1] = 2 * (x[i * 2 + 1] - point.y())

        n = len(self.points) * 2
        for i, constraint in enumerate(self.constraints):
            constraint.apply(self, x, y, n + i)

        return y

    def size(self) -> int:
        return len(self.points) * 2 + len(self.constraints)

    @property
    def x0(self) -> np.ndarray:
        size = self.size()
        x = np.zeros(size, np.float)
        for i, point in enumerate(self.points):
            x[i * 2 + 0] = point.x()
            x[i * 2 + 1] = point.y()
        return x

    def solve(self, rounded: int = ROUNDED) -> np.ndarray:
        opt = {'maxfev': 1000, 'xtol': 1e-4, 'full_output': True}
        output = fsolve(self.system, self.x0, **opt)
        solution, info, status, message = output
        if status != 1:
            raise SolutionNotFound(info, message)
        return solution.round(rounded)

    def recount(self, rounded: int = ROUNDED) -> Points:
        solution = self.solve(rounded)
        for i, point in enumerate(self.points):
            point.setX(solution[i * 2 + 0])
            point.setY(solution[i * 2 + 1])
        return self.points


class SolutionNotFound(Exception):

    def __init__(self, info: dict, message: str):
        self.info = info
        self.message = message

    def __str__(self) -> str:
        return self.message


def main():
    solver = Solver()

    points = [
        Point(1, 1),  # 0
        Point(2, 2),  # 1
        Point(3, 3),  # 2
        Point(4, 4),  # 3
        Point(5, 5),  # 4
    ]

    constraints = [
        FixingY(points[0], 0),
        FixingX(points[0], 0),

        FixingX(points[1], 0),

        Vertical(points[0], points[1]),
        Length(points[0], points[1], 10),

        Horizontal(points[1], points[2]),
        Length(points[1], points[2], 10),

        Length(points[2], points[3], 10),
        Parallel(points[0], points[1], points[3], points[2]),

        Parallel(points[1], points[2], points[3], points[4]),
        Length(points[3], points[4], 10),
    ]

    solver.points.extend(points)
    solver.constraints.extend(constraints)

    return solver.solve()


if __name__ == '__main__':
    start = time()
    sol = main()
    stop = time()

    print(sol)
    print(f'Time: {stop - start}')

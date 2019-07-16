from abc import abstractmethod

import numpy as np

from time import time
from typing import List
from scipy.optimize import fsolve
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


class LengthConstraint(Constraint):

    def __init__(self, line: Line, length: float):
        self.line = line
        self.length = length


class HorizontalConstraint(Constraint):

    def __init__(self, line: Line):
        self.line = line


class VerticalConstraint(Constraint):

    def __init__(self, line: Line):
        self.line = line


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


class CoincidentConstraint(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2


class ParallelConstraint(Constraint):

    def __init__(self, first: Line, second: Line):
        self.first = first
        self.second = second


class PerpendicularConstraint(Constraint):

    def __init__(self, first: Line, second: Line):
        self.first = first
        self.second = second


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

    def solve(self) -> np.ndarray:
        opt = {'maxfev': 10000, 'xtol': 1e-20, 'full_output': True}
        output = fsolve(self.system, self.x0, **opt)
        solution, info, status, message = output
        if status != 1:
            raise SolutionNotFound(info, message)
        return solution.round(ROUNDED)


class SolutionNotFound(Exception):

    def __init__(self, info: dict, message: str):
        self.info = info
        self.message = message

    def __str__(self) -> str:
        return self.message


def main():
    solver = Solver()

    points = [
        Point(10, 10),
        Point(10, 20),
        Point(20, 10),
        Point(20, 20),
    ]

    constraints = [
        # Fixing first point
        FixingX(points[0], 15),
        FixingY(points[0], 15),

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

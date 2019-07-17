from abc import abstractmethod

import numpy as np

from typing import List
from scipy.optimize import fsolve
from PySide2.QtCore import QLineF, QPointF


Line = QLineF
Point = QPointF

Array = np.ndarray

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
        dist = np.abs(square) / line.length()
        return np.round(dist, rounded)
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


def angleTo(l1: Line, l2: Line, rounded: int = ROUNDED):
    value = l1.angleTo(l2)
    return np.round(value, rounded)


class Constraint(object):

    @abstractmethod
    def apply(self, solver, x: Array, y: Array, n: int):   # pragma: no cover
        pass


class Length(Constraint):

    def __init__(self, p1: Point, p2: Point, length: float):
        self.p1 = p1
        self.p2 = p2
        self.length = length

    def apply(self, solver, x: Array, y: Array, n: int):
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

    def apply(self, solver, x: Array, y: Array, n: int):
        i1 = solver.points.index(self.p1) * 2 + 1
        i2 = solver.points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class Vertical(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, solver, x: Array, y: Array, n: int):
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

    def apply(self, solver, x: Array, y: Array, n: int):
        i1 = solver.points.index(self.p1) * 2
        i2 = solver.points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class CoincidentY(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, solver, x: Array, y: Array, n: int):
        i1 = solver.points.index(self.p1) * 2 + 1
        i2 = solver.points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class Parallel(Constraint):

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def apply(self, solver, x: Array, y: Array, n: int):
        i1 = solver.points.index(self.p1) * 2
        i2 = solver.points.index(self.p2) * 2
        i3 = solver.points.index(self.p3) * 2
        i4 = solver.points.index(self.p4) * 2

        ax = x[i1] - x[i2]
        bx = x[i3] - x[i4]
        ay = x[i1 + 1] - x[i2 + 1]
        by = x[i3 + 1] - x[i4 + 1]

        y[i1] += x[n] * by
        y[i2] -= x[n] * by
        y[i3] -= x[n] * ay
        y[i4] += x[n] * ay

        y[i1 + 1] -= x[n] * bx
        y[i2 + 1] += x[n] * bx
        y[i3 + 1] += x[n] * ax
        y[i4 + 1] -= x[n] * ax

        y[n] = ax * by - ay * bx


class Angle(Constraint):

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point, degrees):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.degrees = degrees

    @property
    def radians(self) -> float:
        return np.pi / 180 * self.degrees

    def apply(self, solver, x: Array, y: Array, n: int):
        i1 = solver.points.index(self.p1) * 2
        i2 = solver.points.index(self.p2) * 2
        i3 = solver.points.index(self.p3) * 2
        i4 = solver.points.index(self.p4) * 2

        ax = x[i1] - x[i2]
        bx = x[i3] - x[i4]
        ay = x[i1 + 1] - x[i2 + 1]
        by = x[i3 + 1] - x[i4 + 1]

        l1 = np.sqrt(ax ** 2 + ay ** 2)
        l2 = np.sqrt(bx ** 2 + by ** 2)

        y[i1] += x[n] * (ay * (bx * ay - ax * by) / (l1 ** 3 * l2))
        y[i2] += x[n] * (ay * (ax * by - bx * ay) / (l1 ** 3 * l2))
        y[i3] += x[n] * (by * (ax * by - bx * ay) / (l1 * l2 ** 3))
        y[i4] += x[n] * (by * (bx * ay - ax * by) / (l1 * l2 ** 3))

        y[i1 + 1] += x[n] * (ax * (ax * by - bx * ay) / (l1 ** 3 * l2))
        y[i2 + 1] += x[n] * (ax * (bx * ay - ax * by) / (l1 ** 3 * l2))
        y[i3 + 1] += x[n] * (bx * (bx * ay - ax * by) / (l1 * l2 ** 3))
        y[i4 + 1] += x[n] * (bx * (ax * by - bx * ay) / (l1 * l2 ** 3))

        y[n] = (ax * bx + ay * by) / (l1 * l2) - np.cos(self.radians)


class Perpendicular(Angle):

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__(p1, p2, p3, p4, 90)


Points = List[Point]
Constraints = List[Constraint]


class Solver(object):

    def __init__(self):
        self.points: Points = []
        self.constraints: Constraints = []

    def addPoint(self, point: Point) -> None:
        self.points.append(point)

    def addConstraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)

    def system(self, x: Array) -> Array:
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
    def x0(self) -> Array:
        size = self.size()
        x = np.zeros(size, np.float)
        for i, point in enumerate(self.points):
            x[i * 2 + 0] = point.x()
            x[i * 2 + 1] = point.y()
        return x

    def solve(self, rounded: int = ROUNDED) -> Array:
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

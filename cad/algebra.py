import numpy as np

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


class FixConstraint(Constraint):

    def __init__(self, point: Point, lock: Point):
        self.point = point
        self.lock = lock


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


class System(object):

    def __init__(self):
        self.points: Points = []
        self.constraints: Constraints = []

    def system(self, x: np.ndarray) -> np.ndarray:
        return x

    @property
    def x0(self) -> np.ndarray:
        pass

    def solve(self) -> np.ndarray:
        opt = {'maxfev': 1000, 'xtol': 1e-4, 'full_output': True}
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

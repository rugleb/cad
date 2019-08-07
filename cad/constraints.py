from abc import abstractmethod
from typing import List

import numpy as np

from cad.core import Point

Points = List[Point]

Array = np.ndarray


class Constraint(object):    # pragma: no cover

    @abstractmethod
    def apply(self, points: Points, x: Array, y: Array, n: int):
        pass


Constraints = List[Constraint]


class Length(Constraint):

    def __init__(self, p1: Point, p2: Point, length: float):
        self.p1 = p1
        self.p2 = p2
        self.length = length

    def apply(self, points: Points, x: Array, y: Array, n: int):
        i1 = points.index(self.p1) * 2
        i2 = points.index(self.p2) * 2

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

    def apply(self, points: Points, x: Array, y: Array, n: int):
        i1 = points.index(self.p1) * 2 + 1
        i2 = points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class Vertical(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, points: Points, x: Array, y: Array, n: int):
        i1 = points.index(self.p1) * 2
        i2 = points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class FixingX(Constraint):

    def __init__(self, point: Point, lock: float):
        self.point = point
        self.lock = lock

    def apply(self, points: Points, x: list, y: list, n: int):
        i = points.index(self.point) * 2

        y[i] += x[n]

        y[n] = x[i] - self.lock


class FixingY(Constraint):

    def __init__(self, point: Point, lock: float):
        self.point = point
        self.lock = lock

    def apply(self, points: Points, x: list, y: list, n: int):
        i = points.index(self.point) * 2 + 1

        y[i] += x[n]

        y[n] = x[i] - self.lock


class CoincidentX(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, points: Points, x: Array, y: Array, n: int):
        i1 = points.index(self.p1) * 2
        i2 = points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class CoincidentY(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, points: Points, x: Array, y: Array, n: int):
        i1 = points.index(self.p1) * 2 + 1
        i2 = points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class Parallel(Constraint):

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def apply(self, points: Points, x: Array, y: Array, n: int):
        i1 = points.index(self.p1) * 2
        i2 = points.index(self.p2) * 2
        i3 = points.index(self.p3) * 2
        i4 = points.index(self.p4) * 2

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

    def apply(self, points: Points, x: Array, y: Array, n: int):
        i1 = points.index(self.p1) * 2
        i2 = points.index(self.p2) * 2
        i3 = points.index(self.p3) * 2
        i4 = points.index(self.p4) * 2

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

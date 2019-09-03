from abc import abstractmethod
from numpy import ndarray, cos, pi, sqrt
from typing import List

from cad.core import Point

Index = int
Points = List[Point]


class Constraint(object):

    @abstractmethod
    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        pass


Constraints = List[Constraint]


class LengthConstraint(Constraint):

    def __init__(self, i1: Index, i2: Index, length: float):
        self.i1 = i1
        self.i2 = i2
        self.length = length

    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        dx = x[self.i2 + 0] - x[self.i1 + 0]
        dy = x[self.i2 + 1] - x[self.i1 + 1]

        y[self.i2] += 2 * x[n] * dx
        y[self.i1] -= 2 * x[n] * dx

        y[self.i2 + 1] += 2 * x[n] * dy
        y[self.i1 + 1] -= 2 * x[n] * dy

        y[n] = dx ** 2 + dy ** 2 - self.length ** 2


class HorizontalConstraint(Constraint):

    def __init__(self, i1: Index, i2: Index):
        self.i1 = i1
        self.i2 = i2

    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        y[self.i2] += x[n]
        y[self.i1] -= x[n]

        y[n] = x[self.i2] - x[self.i1]


class VerticalConstraint(Constraint):

    def __init__(self, i1: Index, i2: Index):
        self.i1 = i1
        self.i2 = i2

    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        y[self.i2] += x[n]
        y[self.i1] -= x[n]

        y[n] = x[self.i2] - x[self.i1]


class FixedConstraint(Constraint):

    def __init__(self, i: Index, lock: float):
        self.i = i
        self.lock = lock

    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        y[self.i] += x[n]

        y[n] = x[self.i] - self.lock


class CoincidentConstraint(Constraint):

    def __init__(self, i1: Index, i2: Index):
        self.i1 = i1
        self.i2 = i2

    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        y[self.i2] += x[n]
        y[self.i1] -= x[n]

        y[n] = x[self.i2] - x[self.i1]


class ParallelConstraint(Constraint):

    def __init__(self, i1: Index, i2: Index, i3: Index, i4: Index):
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3
        self.i4 = i4

    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        ax = x[self.i1] - x[self.i2]
        bx = x[self.i3] - x[self.i4]
        ay = x[self.i1 + 1] - x[self.i2 + 1]
        by = x[self.i3 + 1] - x[self.i4 + 1]

        y[self.i1] += x[n] * by
        y[self.i2] -= x[n] * by
        y[self.i3] -= x[n] * ay
        y[self.i4] += x[n] * ay

        y[self.i1 + 1] -= x[n] * bx
        y[self.i2 + 1] += x[n] * bx
        y[self.i3 + 1] += x[n] * ax
        y[self.i4 + 1] -= x[n] * ax

        y[n] = ax * by - ay * bx


class AngleConstraint(Constraint):

    def __init__(self, i1: Index, i2: Index, i3: Index, i4: Index, degrees):
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3
        self.i4 = i4
        self.angle = cos(pi / 180 * degrees)

    def resolve(self, x: ndarray, y: ndarray, n: Index) -> None:
        ax = x[self.i1] - x[self.i2]
        bx = x[self.i3] - x[self.i4]
        ay = x[self.i1 + 1] - x[self.i2 + 1]
        by = x[self.i3 + 1] - x[self.i4 + 1]

        l1 = sqrt(ax ** 2 + ay ** 2)
        l2 = sqrt(bx ** 2 + by ** 2)

        y[self.i1] += x[n] * ay * (bx * ay - ax * by) / (l1 ** 3 * l2)
        y[self.i2] += x[n] * ay * (ax * by - bx * ay) / (l1 ** 3 * l2)
        y[self.i3] += x[n] * by * (ax * by - bx * ay) / (l1 * l2 ** 3)
        y[self.i4] += x[n] * by * (bx * ay - ax * by) / (l1 * l2 ** 3)

        y[self.i1 + 1] += x[n] * ax * (ax * by - bx * ay) / (l1 ** 3 * l2)
        y[self.i2 + 1] += x[n] * ax * (bx * ay - ax * by) / (l1 ** 3 * l2)
        y[self.i3 + 1] += x[n] * bx * (bx * ay - ax * by) / (l1 * l2 ** 3)
        y[self.i4 + 1] += x[n] * bx * (ax * by - bx * ay) / (l1 * l2 ** 3)

        y[n] = (ax * bx + ay * by) / (l1 * l2) - self.angle


class PerpendicularConstraint(AngleConstraint):

    def __init__(self, i1: Index, i2: Index, i3: Index, i4: Index):
        super().__init__(i1, i2, i3, i4, 90)

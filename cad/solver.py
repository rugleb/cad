from typing import List

import numpy as np

from scipy.optimize import fsolve

from cad.core import Point
from cad.constraints import Constraints, Constraint


class Solver(object):

    def __init__(self):
        self.points: List[Point] = []
        self.constraints: Constraints = []

    def addPoint(self, point: Point) -> None:
        self.points.append(point)

    def addConstraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)

    def system(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros(x.shape, x.dtype)

        for i, point in enumerate(self.points):
            y[i * 2 + 0] = 2 * (x[i * 2 + 0] - point.x())
            y[i * 2 + 1] = 2 * (x[i * 2 + 1] - point.y())

        n = len(self.points) * 2
        for i, constraint in enumerate(self.constraints):
            constraint.resolve(x, y, n + i)

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
        opt = {'maxfev': 1000, 'xtol': 1e-4, 'full_output': True}
        output = fsolve(self.system, self.x0, **opt)
        solution, info, status, message = output
        if status != 1:
            raise SolutionNotFound(info, message)
        return solution

    def recount(self) -> List[Point]:
        solution = self.solve().round()
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

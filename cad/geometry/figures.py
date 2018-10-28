from abc import ABC

from .constraints import Constraint
from .exceptions import GivenTypeIsInvalidException


class Figure(ABC):

    def __init__(self):
        self._name = None
        self._constraints = []

    def setName(self, name):
        self._checkName(name)
        self._name = name

    def getName(self):
        return self._name

    def hasName(self):
        return type(self._name) is not None

    @classmethod
    def _checkName(cls, name):
        if type(name) is not str:
            message = 'Figure name must be a string instance.'
            raise GivenTypeIsInvalidException(message)

    def setConstraint(self, constraint):
        # Let's check the object for normal type
        self._checkConstraint(constraint)

        # After validation, we need to remove all previously
        # imposed restrictions with the same type
        for c in self._constraints:
            if type(c) is type(constraint):
                self._constraints.remove(c)

        # Then we just impose this restriction
        self._constraints.append(constraint)

    @classmethod
    def _checkConstraint(cls, constraint):
        if type(constraint) is not Constraint:
            message = 'Figure constraint must be a Constraint instance.'
            raise GivenTypeIsInvalidException(message)

    def getConstraints(self):
        return self._constraints

    def hasConstraints(self):
        return [] == self.getConstraints()


class Point(Figure):

    def __init__(self):
        super().__init__()

        self._x = None
        self._y = None

    def setX(self, x):
        self._checkCoordinate(x)
        self._x = x

    def setY(self, y):
        self._checkCoordinate(y)
        self._y = y

    @classmethod
    def _checkCoordinate(cls, coordinate):
        if type(coordinate) not in (float, int):
            message = 'Point coordinate must be int or float instance.'
            raise GivenTypeIsInvalidException(message)


class Line(Figure):

    def __init__(self):
        super().__init__()

        self._p1 = None
        self._p2 = None

    def setP1(self, point):
        self._checkPoint(point)
        self._p1 = point

    def getP1(self):
        return self._p1

    def hasP1(self):
        return self.getP1() is not None

    def setP2(self, point):
        self._checkPoint(point)
        self._p2 = point

    def getP2(self):
        return self._p2

    def hasP2(self):
        return self.getP2() is not None

    @classmethod
    def _checkPoint(cls, point):
        if type(point) is not Point:
            message = 'Line point must be Point instance.'
            raise GivenTypeIsInvalidException(message)

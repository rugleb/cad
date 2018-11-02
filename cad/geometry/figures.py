from abc import ABC

from PyQt5.QtCore import QPointF, QLineF

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
            msg = 'The figure name must be an instance of string'
            raise GivenTypeIsInvalidException(msg)

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
            msg = 'The constraint must be an instance of the Constraint class'
            raise GivenTypeIsInvalidException(msg)

    def getConstraints(self):
        return self._constraints

    def hasConstraints(self):
        return [] == self.getConstraints()


class PointFigure(Figure):

    def __init__(self):
        super().__init__()

        self._x = None
        self._y = None

    def setX(self, x):
        self._checkCoordinate(x)
        self._x = x

    def getX(self):
        return self._x

    def setY(self, y):
        self._checkCoordinate(y)
        self._y = y

    def getY(self):
        return self._y

    @classmethod
    def _checkCoordinate(cls, coordinate):
        if type(coordinate) not in (float, int):
            msg = 'The point coordinate must be an instance of int or float'
            raise GivenTypeIsInvalidException(msg)

    def toQtPoint(self):
        x = self.getX()
        y = self.getY()
        return QPointF(x, y)


class LineFigure(Figure):

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

    def getX1(self):
        return self.getP1().getX()

    def getY1(self):
        return self.getP1().getY()

    def getX2(self):
        return self.getP2().getX()

    def getY2(self):
        return self.getP2().getY()

    @classmethod
    def _checkPoint(cls, point):
        if type(point) is not PointFigure:
            msg = 'The point must be an instance of the PointFigure class'
            raise GivenTypeIsInvalidException(msg)

    def toQtLine(self):
        p1 = self.getP1()
        p2 = self.getP2()
        return QLineF(p1, p2)

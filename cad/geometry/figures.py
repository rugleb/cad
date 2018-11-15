from abc import ABC

from PyQt5.QtCore import QPointF, QLineF

from .constraints import Constraint
from .exceptions import GivenTypeIsInvalidException


class Figure(ABC):

    def __init__(self):
        self._name = None
        self._constraints = []

    def setName(self, name: str) -> None:
        self._checkName(name)
        self._name = name

    def getName(self) -> str:
        return self._name

    def hasName(self) -> bool:
        return type(self._name) is not None

    @classmethod
    def _checkName(cls, name: str) -> None:
        if type(name) is not str:
            msg = 'The figure name must be an instance of string'
            raise GivenTypeIsInvalidException(msg)

    def setConstraint(self, constraint: Constraint) -> None:
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
    def _checkConstraint(cls, constraint: Constraint) -> None:
        if type(constraint) is not Constraint:
            msg = 'The constraint must be an instance of the Constraint class'
            raise GivenTypeIsInvalidException(msg)

    def getConstraints(self) -> list:
        return self._constraints

    def hasConstraints(self) -> bool:
        return [] == self.getConstraints()


class Point(Figure):

    def __init__(self, x: float, y: float):
        super().__init__()

        self._x = None
        self._y = None

        self.setX(x)
        self.setY(y)

    def setX(self, x: float) -> None:
        self._checkCoordinate(x)
        self._x = x

    def getX(self) -> float:
        return self._x

    def setY(self, y: float) -> None:
        self._checkCoordinate(y)
        self._y = y

    def getY(self) -> float:
        return self._y

    @classmethod
    def _checkCoordinate(cls, coordinate) -> None:
        if type(coordinate) not in (float, int):
            msg = 'The point coordinate must be an instance of int or float'
            raise GivenTypeIsInvalidException(msg)

    def toQtPoint(self) -> QPointF:
        x = self.getX()
        y = self.getY()
        return QPointF(x, y)

    @classmethod
    def fromQtPoint(cls, point: QPointF):
        x = point.x()
        y = point.y()
        return cls(x, y)


class Line(Figure):

    def __init__(self, p1: Point, p2: Point):
        super().__init__()

        self._p1 = None
        self._p2 = None

        self.setP1(p1)
        self.setP2(p2)

    def setP1(self, point: Point) -> None:
        self._checkPoint(point)
        self._p1 = point

    def getP1(self) -> Point:
        return self._p1

    def hasP1(self) -> bool:
        return self.getP1() is not None

    def setP2(self, point: Point) -> None:
        self._checkPoint(point)
        self._p2 = point

    def getP2(self) -> Point:
        return self._p2

    def hasP2(self) -> float:
        return self.getP2() is not None

    def getX1(self) -> float:
        return self.getP1().getX()

    def getY1(self) -> float:
        return self.getP1().getY()

    def getX2(self) -> float:
        return self.getP2().getX()

    def getY2(self) -> float:
        return self.getP2().getY()

    @classmethod
    def _checkPoint(cls, point) -> None:
        if type(point) is not Point:
            msg = 'The point must be an instance of the Point class'
            raise GivenTypeIsInvalidException(msg)

    def toQtLine(self) -> QLineF:
        p1 = self.getP1().toQtPoint()
        p2 = self.getP2().toQtPoint()
        return QLineF(p1, p2)

    @classmethod
    def fromQtLine(cls, line: QLineF):
        p1 = Point.fromQtPoint(line.p1())
        p2 = Point.fromQtPoint(line.p2())
        return cls(p1, p2)

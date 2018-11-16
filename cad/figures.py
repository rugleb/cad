from abc import ABC, abstractmethod

from PyQt5.QtCore import QPointF, QLineF
from contracts import contract

from cad.constraints import Constraint
from cad.math import distancePointToVector


class Figure(ABC):

    def __init__(self):
        self._name = None
        self._constraints = []

    @contract(name=str)
    def setName(self, name: str) -> None:
        self._name = name

    def getName(self) -> str:
        return self._name

    def hasName(self) -> bool:
        return type(self._name) is not None

    @contract(constraint=Constraint)
    def setConstraint(self, constraint: Constraint) -> None:
        # First of all, we need to remove all previously
        # imposed restrictions with the same type
        for c in self._constraints:
            if type(c) is type(constraint):
                self._constraints.remove(c)

        # Then we just impose this restriction
        self._constraints.append(constraint)

    def getConstraints(self) -> list:
        return self._constraints

    def hasConstraints(self) -> bool:
        return [] == self.getConstraints()

    @abstractmethod
    def isEqual(self, figure) -> bool:
        pass


class Point(Figure):

    def __init__(self, x: float, y: float):
        super().__init__()

        self._x = None
        self._y = None

        self.setX(x)
        self.setY(y)

    def setX(self, x: float) -> None:
        self._x = x

    def getX(self) -> float:
        return self._x

    def setY(self, y: float) -> None:
        self._y = y

    def getY(self) -> float:
        return self._y

    def toQtPoint(self) -> QPointF:
        x = self.getX()
        y = self.getY()
        return QPointF(x, y)

    @classmethod
    @contract(point=QPointF)
    def fromQtPoint(cls, point: QPointF):
        x = point.x()
        y = point.y()
        return cls(x, y)

    def isEqual(self, point) -> bool:
        if type(point) is QPointF:
            return self.toQtPoint() == point
        if type(point) is Point:
            return self.toQtPoint() == point.toQtPoint()
        return False


class Line(Figure):

    @contract(p1=Point, p2=Point)
    def __init__(self, p1: Point, p2: Point):
        super().__init__()

        self._p1 = None
        self._p2 = None

        self.setP1(p1)
        self.setP2(p2)

    @contract(point=Point)
    def setP1(self, point: Point) -> None:
        self._p1 = point

    def getP1(self) -> Point:
        return self._p1

    def hasP1(self) -> bool:
        return self.getP1() is not None

    @contract(point=Point)
    def setP2(self, point: Point) -> None:
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

    def toQtLine(self) -> QLineF:
        p1 = self.getP1().toQtPoint()
        p2 = self.getP2().toQtPoint()
        return QLineF(p1, p2)

    @classmethod
    @contract(line=QLineF)
    def fromQtLine(cls, line: QLineF):
        p1 = Point.fromQtPoint(line.p1())
        p2 = Point.fromQtPoint(line.p2())
        return cls(p1, p2)

    def isEqual(self, line) -> bool:
        if type(line) is QLineF:
            return self.toQtLine() == line
        if type(line) is Line:
            return self.toQtLine() == line.toQtLine()
        return False

    def hasPoint(self, p: Point) -> bool:
        d = distancePointToVector(p.toQtPoint(), self.toQtLine())
        if d < 4:
            if self.getX1() < p.getX() < self.getX2():
                return True
            if self.getX2() < p.getX() < self.getX1():
                return True
        return False

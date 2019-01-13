from abc import ABC

from PyQt5.QtCore import QPointF, QLineF
from contracts import contract


class Figure(ABC):
    pass


class Point(Figure):

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    @contract(y=float)
    def y(self, y: float):
        self.__y = y

    @x.setter
    @contract(x=float)
    def x(self, x: float):
        self.__x = x

    @classmethod
    def fromQtPoint(cls, point: QPointF):
        return cls(point.x(), point.y())


class Line(Figure):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    @property
    def p1(self) -> Point:
        return self.__p1

    @property
    def p2(self) -> Point:
        return self.__p2

    @p1.setter
    @contract(p1=Point)
    def p1(self, p1: Point):
        self.__p1 = p1

    @p2.setter
    @contract()
    def p2(self, p2: Point):
        self.__p2 = p2

    @classmethod
    @contract(line=QLineF)
    def fromQtLine(cls, line: QLineF):
        p1 = Point.fromQtPoint(line.p1())
        p2 = Point.fromQtPoint(line.p2())
        return cls(p1, p2)

from PyQt5.QtCore import QPointF, QLineF


class Point:
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
    def y(self, y: float):
        self.__y = y

    @x.setter
    def x(self, x: float):
        self.__x = x

    @property
    def coordinates(self) -> tuple:
        return self.x, self.y

    def toQtPoint(self) -> QPointF:
        return QPointF(self.x, self.y)

    @classmethod
    def fromQtPoint(cls, point: QPointF):
        return cls(point.x(), point.y())


class Line:
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
    def p1(self, p1: Point):
        self.__p1 = p1

    @p2.setter
    def p2(self, p2: Point):
        self.__p2 = p2

    @property
    def points(self) -> tuple:
        return self.p1, self.p2

    def coordinates(self) -> tuple:
        return self.p1.x, self.p1.x, self.p2.x, self.p2.y

    def toQtLine(self) -> QLineF:
        p1 = self.p1.toQtPoint()
        p2 = self.p2.toQtPoint()
        return QLineF(p1, p2)

    @property
    def length(self) -> float:
        return self.toQtLine().length()

    @property
    def dx(self) -> float:
        return self.toQtLine().dx()

    @property
    def dy(self) -> float:
        return self.toQtLine().dy()

    @property
    def x1(self) -> float:
        return self.p1.x

    @property
    def x2(self) -> float:
        return self.p2.x

    @property
    def y1(self) -> float:
        return self.p1.y

    @property
    def y2(self) -> float:
        return self.p2.y

    @classmethod
    def fromQtLine(cls, line: QLineF):
        p1 = Point.fromQtPoint(line.p1())
        p2 = Point.fromQtPoint(line.p2())
        return cls(p1, p2)

    def distToPoint(self, p: Point) -> float:
        s = self.dy * p.x - self.dx * p.y + self.x2 * self.y1 - self.y2 * self.x1
        return abs(s) / self.length

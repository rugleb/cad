import math

from PySide2.QtCore import QLineF, QPointF


Line = QLineF
Point = QPointF


ROUNDED = 2


def sqrt(x: float, rounded: int = ROUNDED) -> float:
    return round(math.sqrt(x), rounded)


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

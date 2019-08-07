import numpy as np

from PySide2.QtCore import QLineF, QPointF


Line = QLineF
Point = QPointF


ROUNDED = 2
INACCURACY = 2


def sqrt(x: float) -> float:
    return np.sqrt(x)


def p2p(p1: Point, p2: Point) -> float:
    """Returns the distance between two points.

    :param Point p1: Starting point
    :param Point p2: Ending point
    :return: distance between two points
    :rtype: float
    """

    return Line(p1, p2).length()


def p2l(point: Point, line: Point, rounded: int = ROUNDED) -> float:
    if line.length() > 0:
        x0, y0 = point.x(), point.y()
        x1, y1 = line.x1(), line.y1()
        x2, y2 = line.x2(), line.y2()
        square = (y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1
        dist = np.abs(square) / line.length()
        return np.round(dist, rounded)
    else:
        return p2p(line.p1(), point)


def p2s(point: Point, line: Line, rounded: int = ROUNDED) -> float:
    if line.x1() == line.x2():
        return p2l(point, line)
    if line.x1() > line.x2():
        line = Line(line.p2(), line.p1())
    if line.x1() <= point.x() <= line.x2():
        return p2l(point, line, rounded)
    if line.x2() < point.x():
        return p2p(line.p2(), point)
    return p2p(line.p1(), point)


def angleTo(l1: Line, l2: Line, rounded: int = ROUNDED):
    value = l1.angleTo(l2)
    return np.round(value, rounded)

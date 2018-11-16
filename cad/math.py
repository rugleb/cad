from PyQt5.QtCore import QLineF, QPointF


def distancePointToPoint(p1: QPointF, p2: QPointF) -> float:
    return QLineF(p1, p2).length()


def distancePointToVector(p: QPointF, l: QLineF) -> float:
    if not l.length() > 0:
        return distancePointToPoint(p, l.p1())
    s = l.dy() * p.x() - l.dx() * p.y() + l.x2() * l.y1() - l.y2() * l.x1()
    return abs(s) / l.length()


def isPointOnVector(p: QPointF, l: QLineF) -> bool:
    return distancePointToVector(p, l) == 0.


def isPointOnLine(p: QPointF, l: QLineF) -> bool:
    if isPointOnVector(p, l):
        return l.x1() <= p.x() <= l.x2()
    return False

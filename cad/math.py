from cad.figures import Line, Point


def distPointToVector(p: Point, l: Line) -> float:
    if not l.length > 0:
        return Line(p, l.p1).length
    s = l.dy * p.x - l.dx * p.y + l.x2 * l.y1 - l.y2 * l.x1
    return abs(s) / l.length


def isPointOnVector(p: Point, l: Line) -> bool:
    return distPointToVector(p, l) == 0.


def isPointOnLine(p: Point, l: Line) -> bool:
    if isPointOnVector(p, l):
        return l.x1 <= p.x <= l.x2
    return False

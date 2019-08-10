from cad.core import Segment, Point


def dotProduct(p1: Point, p2: Point) -> float:
    """Returns the dot product of p1 and p2.

    :param Point p1: First point
    :param Point p2: Second point
    :return: Dot product of p1 and p2
    """

    return Point.dotProduct(p1, p2)


def p2p(p1: Point, p2: Point) -> float:
    """Returns the distance between two points.

    :param Point p1: First point
    :param Point p2: Second point
    :return: Distance between two points
    """

    return Segment(p1, p2).length()


def p2l(point: Point, segment: Segment) -> float:
    """Returns the distance between point and line.

    :param Point point:
    :param Segment segment:
    :return: Distance between point and line
    """

    if segment.length() > 0:
        x0, y0 = point.coordinates()
        x1, y1, x2, y2 = segment.coordinates()
        square = (y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1
        return abs(square) / segment.length()

    return p2p(segment.p1(), point)


def p2s(point: Point, segment: Segment) -> float:
    """Returns the distance between point and segment.

    :param Point point:
    :param Segment segment:
    :return: Distance between point and segment
    """

    p1, p2 = segment.points()

    v = p2 - p1
    w = point - p1

    c1 = dotProduct(w, v)
    if c1 <= 0:
        return p2p(point, p1)

    c2 = dotProduct(v, v)
    if c2 <= c1:
        return p2p(point, p2)

    p = p1 + c1 / c2 * v
    return p2p(point, p)


def angle(s1: Segment, s2: Segment) -> float:
    """Returns tha angle between s1 and s2 in degrees.

    :param Segment s1:
    :param Segment s2:
    :return: Angle between s1 and s2
    """

    return s1.angleTo(s2)

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import Generator

from PySide2.QtGui import QPainter, QColor, QPen, QBrush
from PySide2.QtCore import QPointF, QObject, Qt, QLineF, Signal


class Color(QColor):
    pass


class Point(QPointF):

    def coordinates(self) -> tuple:
        """Returns the tuple of coordinates.

        :return: Point coordinates
        :rtype: tuple
        """

        return self.x(), self.y()


class Segment(QLineF):
    """The Segment class represents a two-dimensional segment
    on a plane using floating-point precision.
    """

    def isVertical(self) -> bool:
        """Checks if the segment is vertical.

        :return: Vertical or not
        :rtype: bool
        """

        return self.x1() == self.x2()

    def isHorizontal(self) -> bool:
        """Checks if the segment is horizontal.

        :return: Horizontal or not
        :rtype: bool
        """

        return self.y1() == self.y2()

    def points(self) -> tuple:
        """Returns the tuple of points.

        :return: Segment points
        :rtype: tuple
        """

        return self.p1(), self.p2()

    def coordinates(self) -> tuple:
        """Returns the tuple of coordinates.

        :return: Segment coordinates
        :rtype: tuple
        """

        return self.x1(), self.y1(), self.x2(), self.y2()


class Pen(QPen):
    pass


class Brush(QBrush):
    pass


class Painter(QPainter):

    def drawCircle(self, center: Point, radius: float) -> None:
        """Draws the circle positioned at center with a given radius.

        :param Point center: Circle center
        :param Radius radius: Circle radius
        :return: None
        """

        return self.drawEllipse(center, radius, radius)

    def drawSegment(self, segment: Segment) -> None:
        """Draws a segment using the current pen.

        :param Segment segment:
        :return: None
        """

        return self.drawLine(segment)


class DrawStyle(Enum):
    """This enum type defines the drawing styles used in this CAD.

    For uniformity of display of objects, it is necessary to use
    only those styles which are described in this class.
    """

    def __new__(cls, color: Color, width: float):
        obj = object.__new__(cls)
        obj._width = width
        obj._color = color
        return obj

    def width(self) -> float:
        return self._width

    def color(self) -> Color:
        return self._color

    Default = Color(54, 93, 171), 5.         # default drawing style
    Highlight = Color(254, 137, 144), 6.     # style for selected objects


class Drawable(QObject):
    """The Drawable interface.

    This class defines the interface for manipulation of drawable objects.
    """

    styleChanged = Signal()

    def __init__(self, geometry: QObject, style: DrawStyle):
        super().__init__()

        self._geometry = geometry
        self._style = style

        self._tracking = True

    def geometry(self) -> QObject:
        """Return geometry of the object.

        :return: Geometry of the object
        :rtype: QObject
        """

        return self._geometry

    def style(self) -> DrawStyle:
        """Return the drawing style of the object.

        :return: Drawing style
        :rtype: DrawStyle
        """

        return self._style

    def setStyle(self, style: DrawStyle) -> None:
        """Edit the drawing style of the object.

        :return: None
        """

        if self.style is not style:
            self._style = style

            self.styleChanged.emit()

    def color(self) -> Color:
        """Return the color of the invoking object.

        :return: The color of the object
        :rtype: QColor
        """

        return self.style().color()

    def width(self) -> float:
        """Return the drawing brush width of the object.

        :return: The width of the brush
        :rtype: float
        """

        return self.style().width()

    def highlight(self) -> None:
        """Highlight the object.

        :return: None
        """

        self.setStyle(DrawStyle.Highlight)

    def unHighlight(self) -> None:
        """Unhighlight the invoking object.

        :return: None
        """

        self.setStyle(DrawStyle.Default)

    def isHighlighted(self) -> bool:
        """Determine if the object is highlighted.

        :return: None
        """

        return self.style() is DrawStyle.Highlight

    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        return Qt.NoPen

    def brush(self) -> Brush:
        """Return the Brush class instance.

        :return: Instance of Brush class
        :rtype: Brush
        """

        return Brush(self.color)

    @abstractmethod
    def draw(self, painter: Painter) -> None:
        """Draws the object by given Painter.

        :param Painter painter:
        :return: None
        """

        pass

    def onMouseMoved(self, cursor: Point) -> None:
        """Handler of the MouseMoved event.

        :param Point cursor:
        :return: None
        """

        if not self.isMouseTracked():
            return None

        if self.isClose(cursor):
            return self.highlight()

        if self.isHighlighted():
            return self.unHighlight()

    @abstractmethod
    def isClose(self, cursor: Point) -> bool:
        """Determines whether the cursor is close to the object.

        :param Point cursor: Cursor position
        :return: Close or not
        """

        pass

    def setMouseTracking(self, status: bool) -> Drawable:
        """Update mouse tracking mode status.

        :param bool status: Enable or not
        :return: self
        """

        self._tracking = status

        return self

    def enableMouseTracking(self) -> Drawable:
        """Enable mouse tracking mode.

        :return: self
        """

        return self.setMouseTracking(True)

    def disableMouseTracking(self) -> Drawable:
        """Disable mouse tracking mode.

        :return: self
        """

        return self.setMouseTracking(False)

    def isMouseTracked(self) -> bool:
        """Checks whether the mouse position is tracked.

        :return: Tracked or not
        """

        return self._tracking


class SmartPoint(Drawable):

    @classmethod
    def fromPoint(cls, point: Point) -> SmartPoint:
        """Creates a new object instance by the given Point.

        :param Point point:
        :return: SmartPoint instance
        """

        return SmartPoint(point, DrawStyle.Default)

    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        return Qt.NoPen

    def point(self) -> Point:
        """Alias for geometry property.

        :return: Instance of Point class
        :rtype: Point
        """

        return self.geometry()

    def draw(self, painter: Painter) -> None:
        """Draws the Point by given Painter.

        :param Painter painter:
        :return: None
        """

        brush = self.color()
        center = self.point()
        radius = self.width()

        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawCircle(center, radius)

    def isClose(self, cursor: Point) -> bool:
        """Determines whether the cursor is close to the object.

        :param Point cursor: Cursor position
        :return: Close or not
        """

        center = self.point()
        radius = self.width()

        return p2p(cursor, center) < radius


class SmartSegment(Drawable):

    @classmethod
    def fromPoint(cls, point: Point) -> SmartSegment:
        """Create a new object instance by the given Point.

        :param Point point:
        :return: SmartPoint instance
        """

        return SmartSegment.fromPoints(point, point)

    @classmethod
    def fromPoints(cls, p1: Point, p2: Point) -> SmartSegment:
        """Create a new object instance by the given Points.

        :param Point p1: Start point
        :param Point p2: End point
        :return: SmartSegment instance
        """

        geometry = Segment(p1, p2)
        return SmartSegment(geometry, DrawStyle.Default)

    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        brush = self.color()
        radius = self.width() / 2

        return Pen(brush, radius)

    def segment(self) -> Segment:
        """Alias for geometry property.

        :return: Instance of Segment class
        :rtype: Segment
        """

        return self.geometry()

    def points(self) -> Generator:
        """Return the Generator of SmartPoints.

        :return: SmartPoints generator
        """

        style = self.style()

        for p in self.segment().points():
            yield SmartPoint(p, style)

    def draw(self, painter: Painter) -> None:
        """Draws the Segment by given Painter.

        :param Painter painter:
        :return: None
        """

        pen = self.pen()
        segment = self.segment()

        painter.setPen(pen)
        painter.drawSegment(segment)

        for point in self.points():
            point.draw(painter)

    def isClose(self, cursor: Point) -> bool:
        """Determines whether the cursor is close to the object.

        :param Point cursor: Cursor position
        :return: Close or not
        """

        radius = self.width() / 2
        segment = self.segment()

        return p2s(cursor, segment) < radius


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

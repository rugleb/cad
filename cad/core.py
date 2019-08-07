from __future__ import annotations

from abc import abstractmethod, ABC
from enum import Enum

from PySide2.QtGui import QPainter, QColor, QPen, QBrush
from PySide2.QtCore import QPointF, QObject, Qt, QLineF

Color = QColor
Point = QPointF
Segment = QLineF


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
        obj.width = width
        obj.color = color
        return obj

    Default = Color(54, 93, 171), 5.         # default drawing style
    Highlight = Color(254,  137, 144), 3.    # style for selected objects


class Drawable(ABC):
    """The Drawable interface.

    This class defines the interface for manipulation of drawable objects.
    """

    def __init__(self, geometry: QObject, style: DrawStyle):
        self._geometry = geometry
        self._style = style

    @property
    def geometry(self) -> QObject:
        """Return geometry of the object.

        :return: Geometry of the object
        :rtype: QObject
        """

        return self._geometry

    @property
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

        self._style = style

    @property
    def color(self) -> Color:
        """Return the color of the invoking object.

        :return: The color of the object
        :rtype: QColor
        """

        return self.style.color

    @property
    def width(self) -> float:
        """Return the drawing brush width of the object.

        :return: The width of the brush
        :rtype: float
        """

        return self.style.width

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

        return self.style is DrawStyle.Highlight

    @property
    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        return Qt.NoPen

    @property
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


class SmartPoint(Drawable):

    @property
    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        return Qt.NoPen

    @property
    def point(self) -> Point:
        """Alias for geometry property.

        :return: Instance of Point class
        :rtype: Point
        """

        return self.geometry

    @property
    def radius(self) -> float:
        """Returns the radius of the drawing brush.

        :return: Drawing brush radius
        :rtype: float
        """

        return self.width * 2

    def draw(self, painter: Painter) -> None:
        """Draws the Point by given Painter.

        :param Painter painter:
        :return: None
        """

        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawCircle(self.point, self.radius)


class SmartSegment(Drawable):

    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        return Pen(self.color, self.width)

    @property
    def segment(self) -> Segment:
        """Alias for geometry property.

        :return: Instance of Segment class
        :rtype: Segment
        """

        return self.geometry

    def draw(self, painter: Painter) -> None:
        """Draws the Segment by given Painter.

        :param Painter painter:
        :return: None
        """

        painter.setPen(self.pen)
        painter.drawSegment(self.segment)

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

    Default = Color(54, 93, 171), 5         # default drawing style
    Highlight = Color(254,  137, 144), 3    # style for selected objects


class Painter(QPainter):

    def drawCircle(self, center: Point, radius: float) -> None:
        """Draws the circle positioned at center with a given radius.

        :param Point center: Circle center
        :param Radius radius: Circle radius
        :return: None
        """

        return self.drawEllipse(center, radius, radius)


class Drawable(ABC):
    """The Drawable interface.

    This class defines the interface for manipulation of drawable objects.
    """

    def __init__(self, geometry: QObject):
        self._geometry = geometry

        self._style = DrawStyle.Default

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

        self._style = style

    def color(self) -> Color:
        """Return the color of the invoking object.

        :return: The color of the object
        :rtype: QColor
        """

        return self.style().color

    def width(self) -> float:
        """Return the drawing brush width of the object.

        :return: The width of the brush
        :rtype: float
        """

        return self.style().width

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

    @abstractmethod
    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        pass

    def brush(self) -> Brush:
        """Return the Brush class instance.

        :return: Instance of Brush class
        :rtype: Brush
        """

        return Brush(self.color())

    @abstractmethod
    def draw(self, painter: Painter) -> None:
        """Draws the object by given Painter.

        :param Painter painter:
        :return: None
        """

        pass


class SmartPoint(Drawable):

    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        return Qt.NoPen

    def draw(self, painter: Painter) -> None:
        """Draws the Point by given Painter.

        :param Painter painter:
        :return: None
        """

        pen = self.pen()
        brush = self.brush()
        center = self.geometry()
        radius = self.width()

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawCircle(center, radius)


class SmartSegment(Drawable):

    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        color = self.color()
        width = self.width()
        return Pen(color, width)

    def draw(self, painter: Painter) -> None:
        """Draws the Segment by given Painter.

        :param Painter painter:
        :return: None
        """

        pen = self.pen()
        segment = self.geometry()

        painter.setPen(pen)
        painter.drawLine(segment)

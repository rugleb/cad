from __future__ import annotations

from abc import abstractmethod, ABC

from PySide2.QtGui import QPainter, QColor, QPen, QBrush
from PySide2.QtCore import QPointF, QObject, Qt

Color = QColor
Point = QPointF

DEFAULT_COLOR = Color(54, 93, 171)
HIGHLIGHT_COLOR = Color(254,  137, 144)

DEFAULT_WIDTH = 3.
HIGHLIGHT_WIDTH = 5.


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


class Drawable(ABC):
    """The Drawable interface.

    This class defines the interface for manipulation of drawable objects.
    """

    def __init__(self, geometry: QObject):
        self._geometry = geometry

        self._width = DEFAULT_WIDTH
        self._color = DEFAULT_COLOR

    def geometry(self) -> QObject:
        """Return geometry of the object.

        :return: Geometry of the object
        :rtype: QObject
        """

        return self._geometry

    def color(self) -> Color:
        """Return the color of the invoking object.

        :return: The color of the object
        :rtype: QColor
        """

        return self._color

    def setColor(self, color: Color) -> None:
        """Edit the color of the object.

        :param QColor color: A new color object
        :return: None
        """

        self._color = color

    def width(self) -> float:
        """Return the drawing brush width of the object.

        :return: The width of the brush
        :rtype: float
        """

        return self._width

    def setWidth(self, width: float) -> None:
        """Edit the line width of the object.

        :param float width: New brush width
        :return: None
        """

        self._width = width

    def highlight(self) -> None:
        """Highlight the object.

        :return: None
        """

        self.setWidth(HIGHLIGHT_WIDTH)
        self.setColor(HIGHLIGHT_COLOR)

    def unHighlight(self) -> None:
        """Unhighlight the invoking object.

        :return: None
        """

        self.setWidth(DEFAULT_WIDTH)
        self.setColor(DEFAULT_COLOR)

    def isHighlighted(self) -> bool:
        """Determine if the object is highlighted.

        :return: None
        """

        if self.width() is HIGHLIGHT_WIDTH:
            if self.color() is HIGHLIGHT_COLOR:
                return True
        return False

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
        """Draws the object by given Painter.

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

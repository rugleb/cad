from __future__ import annotations

from abc import abstractmethod
from typing import NewType

from PySide2.QtGui import QPainter, QColor, QPen, QBrush
from PySide2.QtCore import QPointF

Point = QPointF
Color = QColor

Radius = NewType('Radius', float)

DEFAULT_COLOR = Color(54, 93, 171)
HIGHLIGHT_COLOR = Color(254,  137, 144)

DEFAULT_WIDTH = 3.
HIGHLIGHT_WIDTH = 5.


class Pen(QPen):
    pass


class Brush(QBrush):
    pass


class Painter(QPainter):

    def drawCircle(self, center: Point, radius: Radius) -> None:
        """Draws the circle positioned at center with a given radius.

        :param Point center: Circle center
        :param Radius radius: Circle radius
        :return: None
        """

        return self.drawEllipse(center, radius, radius)


class Drawable:
    """The Drawable interface.

    This class defines the interface for manipulation of CAD drawable objects.
    """

    def color(self) -> Color:
        """Return the color of the invoking object.

        :return: The color of the object
        :rtype: QColor
        """

        pass

    def setColor(self, color: Color) -> None:
        """Edit the color of the object.

        :param QColor color: A new color object
        :return: None
        """

        pass

    def width(self) -> float:
        """Return the drawing brush width of the object.

        :return: The width of the brush
        :rtype: float
        """

        pass

    def setWidth(self, width: float) -> float:
        """Edit the line width of the object.

        :param float width: New brush width
        :return: None
        """

        pass

    def highlight(self) -> None:
        """Highlight the object.

        :return: None
        """

        pass

    def unHighlight(self) -> None:
        """Unhighlight the invoking object.

        :return: None
        """

        pass

    def isHighlighted(self) -> bool:
        """Determine if the object is highlighted.

        :return: None
        """

        pass

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

        pass

    @abstractmethod
    def draw(self, painter: Painter) -> None:
        """Draws the object by given Painter.

        :param Painter painter:
        :return: None
        """

        pass

from __future__ import annotations

from abc import abstractmethod, ABC

from PySide2.QtGui import QPainter, QColor, QPen, QBrush
from PySide2.QtCore import QPointF, QObject, Qt

Point = QPointF
Color = QColor

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

    This class defines the interface for manipulation of CAD drawable objects.
    """

    @abstractmethod
    def geometry(self) -> QObject:
        """Return geometry of the object.

        :return: Geometry of the object
        :rtype: QObject
        """

        pass

    @abstractmethod
    def color(self) -> Color:
        """Return the color of the invoking object.

        :return: The color of the object
        :rtype: QColor
        """

        pass

    @abstractmethod
    def setColor(self, color: Color) -> None:
        """Edit the color of the object.

        :param QColor color: A new color object
        :return: None
        """

        pass

    @abstractmethod
    def width(self) -> float:
        """Return the drawing brush width of the object.

        :return: The width of the brush
        :rtype: float
        """

        pass

    @abstractmethod
    def setWidth(self, width: float) -> None:
        """Edit the line width of the object.

        :param float width: New brush width
        :return: None
        """

        pass

    @abstractmethod
    def highlight(self) -> None:
        """Highlight the object.

        :return: None
        """

        pass

    @abstractmethod
    def unHighlight(self) -> None:
        """Unhighlight the invoking object.

        :return: None
        """

        pass

    @abstractmethod
    def isHighlighted(self) -> bool:
        """Determine if the object is highlighted.

        :return: None
        """

        pass

    @abstractmethod
    def pen(self) -> Pen:
        """Return the Pen class instance.

        :return: Instance of Pen class
        :rtype: Pen
        """

        pass

    @abstractmethod
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

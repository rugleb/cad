from __future__ import annotations

from abc import abstractmethod

from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtCore import QPointF, Qt

Point = QPointF
Color = QColor


DEFAULT_COLOR = Color(54, 93, 171)
HIGHLIGHT_COLOR = Color(254,  137, 144)

DEFAULT_WIDTH = 3.
HIGHLIGHT_WIDTH = 5.


class Pen(QPen):
    pass


class Painter(QPainter):

    def drawCircle(self, center: Point, radius: float) -> None:
        self.drawEllipse(center, radius, radius)


class Drawable:

    @abstractmethod
    def draw(self, painter: Painter) -> None:
        pass

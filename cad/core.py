from __future__ import annotations

from abc import abstractmethod

from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtCore import QPointF, Qt

Point = QPointF
Color = QColor


class Pen(QPen):
    pass


class Painter(QPainter):

    def drawCircle(self, center: Point, radius: float) -> None:
        self.drawEllipse(center, radius, radius)


class Drawable:

    @abstractmethod
    def draw(self, painter: Painter) -> None:
        pass

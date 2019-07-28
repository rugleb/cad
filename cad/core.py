from abc import abstractmethod

from PySide2.QtGui import QPainter
from PySide2.QtCore import QPointF

Point = QPointF


class Painter(QPainter):

    def drawCircle(self, center: Point, radius: float) -> None:
        self.drawEllipse(center, radius, radius)


class Drawable:

    @abstractmethod
    def draw(self, painter: Painter) -> None:
        pass

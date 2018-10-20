from PyQt5 import QtCore, QtGui, QtWidgets

from cad.drawing import Line, Point, Pen


class Sketch(QtWidgets.QWidget):
    _lines = None
    _point = None

    def __init__(self):
        super().__init__()

        self._lines = []
        self._point = None

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')
        self.show()

    def isMousePressed(self):
        return self._point is not None

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self._point = Point(event.localPos())

    def mouseReleaseEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.LeftButton:
                point = Point(event.localPos())
                line = Line(self._point, point)
                self._point = None
                self.draw(line)

    def mouseMoveEvent(self, event):
        point = Point(event.localPos())
        if self.isMousePressed():
            if self._lines:
                self._lines.pop(-1)
            line = Line(self._point, point)
            self._lines.append(line)
        for line in self._lines:
            if line.hasPoint(point):
                line.setPen(Pen.active())
            else:
                line.setPen(Pen.stable())
        self.update()

    def draw(self, line):
        self._lines.append(line)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self._drawLines(painter)
        painter.end()

    def _drawLines(self, painter):
        for line in self._lines:
            pen = line.getPen()
            painter.setPen(pen)
            painter.drawLine(line)
            width = pen.widthF()
            pen.setWidthF(width * 2)
            painter.setPen(pen)
            painter.drawPoints(line.p1(), line.p2())
            pen.setWidthF(width)
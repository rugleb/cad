from PyQt5 import QtCore, QtGui, QtWidgets

from cad.drawing import Line, Point, Pen


class Sketch(QtWidgets.QWidget):
    points = None
    segments = None

    def __init__(self, *args):
        super().__init__(*args)

        self.points = []
        self.segments = []

        self.cursorPos = None
        self.pressedPos = None

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    def isMousePressed(self):
        return self.pressedPos is not None

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.segments = [s for s in self.segments if not s.hasPoint(self.cursorPos)]
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressedPos = event.localPos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            line = Line(self.pressedPos, self.cursorPos)
            self.pressedPos = None
            self.draw(line)

    def mouseMoveEvent(self, event):
        self.cursorPos = event.localPos()
        if self.isMousePressed():
            if self.segments:
                self.segments.pop(-1)
            line = Line(self.pressedPos, self.cursorPos)
            self.segments.append(line)
        for line in self.segments:
            if line.hasPoint(self.cursorPos):
                line.setPen(Pen.active())
            else:
                line.setPen(Pen.stable())
        self.update()

    def draw(self, line):
        self.segments.append(line)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self._drawLines(painter)
        painter.end()

    def _drawLines(self, painter):
        for line in self.segments:
            pen = line.getPen()
            painter.setPen(pen)
            painter.drawLine(line)
            width = pen.widthF()
            pen.setWidthF(width * 2)
            painter.setPen(pen)
            painter.drawPoints(line.p1(), line.p2())
            pen.setWidthF(width)

    def enableAngleScope(self, value):
        pass

    def disableAngleScope(self):
        pass

    def enableLengthScope(self, value):
        pass

    def disableLengthScope(self):
        pass

    def enableParallelsAction(self):
        pass

    def disableParallelsAction(self):
        pass

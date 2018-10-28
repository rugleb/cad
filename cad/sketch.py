from PyQt5 import QtCore, QtGui, QtWidgets

from cad.drawing import Pen
from cad.geometry.constraints import SketchMode


class Sketch(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.points = []
        self.segments = []

        self.currentPos = None
        self.pressedPos = None

        self.mode = SketchMode(self)

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    def isMousePressed(self):
        return self.pressedPos is not None

    def getCurrentPosition(self):
        return self.currentPos

    def getPressedPosition(self):
        return self.pressedPos

    def keyPressEvent(self, event):
        keys = [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete]

        if event.key() in keys:
            segment = self.getSelected()
            if segment:
                self.segments.remove(segment)

        self.update()

    def mousePressEvent(self, event):
        self.pressedPos = event.localPos()

        self.mode.mousePressedHandler()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressedPos = None

        self.update()

    def mouseMoveEvent(self, event):
        self.currentPos = event.localPos()

        self.mode.mouseMovedHandler()

        for segment in self.segments:
            segment.setPen(Pen.stable())

        figure = self.getSelected()
        if figure:
            figure.setPen(Pen.selected())

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawLines(painter)
        self.drawPoints(painter)
        painter.end()

    def drawLines(self, painter):
        for line in self.segments:
            pen = line.getPen()
            painter.setPen(pen)
            painter.drawLine(line)
            width = pen.widthF()
            pen.setWidthF(width * 2)
            painter.setPen(pen)
            painter.drawPoints(line.p1(), line.p2())
            pen.setWidthF(width)

    def drawPoints(self, painter):
        for point in self.points:
            pen = Pen.stable()
            painter.setPen(pen)
            painter.drawPoint(point)

    def getSelected(self):
        for segment in self.segments:
            if segment.hasPoint(self.currentPos):
                return segment
        return None

    def setMode(self, mode):
        if not isinstance(mode, SketchMode):
            message = 'Given type is invalid. Expected SketchMode instance'
            raise Exception(message)
        self.mode = mode

from PyQt5 import QtCore, QtGui, QtWidgets

from cad.solver import *
from cad.math import *


class Sketch(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.lines = []
        self.points = []

        self.currentPos = None
        self.pressedPos = None

        self.handler = LineDrawing()
        self.system = System(self)

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    def addLine(self, line: Line):
        self.lines.append(line)

    def isMousePressed(self) -> bool:
        return self.pressedPos is not None

    def getCurrentPosition(self) -> Point:
        return self.currentPos

    def getPressedPosition(self) -> Point:
        return self.pressedPos

    def getActiveLine(self):
        for line in self.lines:
            if line.distToPoint(self.currentPos) < 4:
                return line
        return False

    def getActivePoint(self):
        for point in self.points:
            if point.distToPoint(self.currentPos) < 4:
                return point
        return False

    def keyPressEvent(self, event):
        keys = [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete]

        if event.key() in keys:
            self.removeSelectedFigure()

        self.update()

    def removeSelectedFigure(self):
        pass

    def mousePressEvent(self, event):
        position = event.localPos()
        self.pressedPos = Point.fromQtPoint(position)

        self.handler.mousePressed(self)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressedPos = None

        self.handler.mouseReleased(self)

    def mouseMoveEvent(self, event):
        position = event.localPos()
        self.currentPos = Point.fromQtPoint(position)

        self.handler.mouseMoved(self)

    def update(self):
        self.system.recount()

        super().update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawLines(painter)
        self.drawPoints(painter)
        painter.end()

    def drawLines(self, painter):
        for line in self.lines:
            pen = QtGui.QPen(QtCore.Qt.gray, 6, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(line.toQtLine())

    def drawPoints(self, painter):
        for point in self.points:
            pen = QtGui.QPen(QtCore.Qt.gray, 6, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.drawPoint(point.toQtPoint())

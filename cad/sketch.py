from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPointF, pyqtSignal, pyqtSlot

from contracts import contract

from cad.constraints import Constraint


class Sketch(QtWidgets.QWidget):

    mousePressedSignal = pyqtSignal(QPointF)
    mouseReleasedSignal = pyqtSignal(QPointF)

    def __init__(self, *args):
        super().__init__(*args)

        self.figures = []

        self.currentPos = None
        self.pressedPos = None

        self.constraint = None

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    @pyqtSlot(Constraint)
    @contract(constraint=Constraint)
    def constraintChanged(self, constraint: Constraint):
        self.constraint = constraint

    def isMousePressed(self):
        return self.pressedPos is not None

    def keyPressEvent(self, event):
        keys = [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete]

        if event.key() in keys:
            self.removeSelectedFigure()

        self.update()

    def removeSelectedFigure(self):
        selected = self.getSelectedFigure()
        if selected is not None:
            self.figures.remove(selected)

    def getSelectedFigure(self):
        for figure in self.figures:
            if figure.hasPoint(self.currentPos):
                return True
        return False

    def mousePressEvent(self, event):
        self.pressedPos = event.localPos()

        self.mousePressedSignal.emit(self.pressedPos)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressedPos = None

        self.mouseReleasedSignal.emit(self.pressedPos)

        self.update()

    def mouseMoveEvent(self, event):
        self.currentPos = event.localPos()

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawLines(painter)
        self.drawPoints(painter)
        painter.end()

    def drawLines(self, painter):
        for line in self.lines:
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

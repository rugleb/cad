from PyQt5 import QtCore, QtGui, QtWidgets


class Sketch(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.lines = []
        self.points = []

        self.currentPos = None
        self.pressedPos = None

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    def isMousePressed(self):
        return self.pressedPos is not None

    def keyPressEvent(self, event):
        keys = [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete]

        if event.key() in keys:
            segment = self.getSelected()
            if segment:
                self.lines.remove(segment)

        self.update()

    def mousePressEvent(self, event):
        self.pressedPos = event.localPos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressedPos = None

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

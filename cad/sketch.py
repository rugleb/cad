from PyQt5 import QtCore, QtGui, QtWidgets

from cad.drawing import Segment, Pen, Point


DRAWING_LINE_MODE = 0
DRAWING_POINT_MODE = 1
ANGLE_SCOPE_MODE = 3
LENGTH_SCOPE_MODE = 4
PARALLELS_SCOPE_MODE = 5


class Sketch(QtWidgets.QWidget):
    points = None
    segments = None

    def __init__(self, *args):
        super().__init__(*args)

        self.points = []
        self.segments = []

        self.cursorPos = None
        self.pressedPos = None

        self.mode = DRAWING_LINE_MODE
        self.scope = None

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    def isMousePressed(self):
        return self.pressedPos is not None

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            for segment in self.segments:
                if segment.hasPoint(self.cursorPos):
                    self.segments.remove(segment)
        self.update()

    def mousePressEvent(self, event):
        self.pressedPos = event.localPos()

        if self.mode == DRAWING_LINE_MODE:
            segment = Segment(self.pressedPos, self.pressedPos)
            self.segments.append(segment)

        if self.mode == DRAWING_POINT_MODE:
            point = Point(self.pressedPos)
            self.points.append(point)

        if self.mode == ANGLE_SCOPE_MODE:
            for segment in self.segments:
                if segment.hasPoint(self.cursorPos):
                    segment.setAngle(self.scope)

        if self.mode == LENGTH_SCOPE_MODE:
            for segment in self.segments:
                if segment.hasPoint(self.cursorPos):
                    segment.setLength(self.scope)

        if self.mode == PARALLELS_SCOPE_MODE:
            if self.scope is None:
                for segment in self.segments:
                    if segment.hasPoint(self.cursorPos):
                        self.scope = segment
                        break
            else:
                for segment in self.segments:
                    if segment.hasPoint(self.cursorPos):
                        segment.setAngle(self.scope.angle())
                        self.scope = None

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressedPos = None

        self.update()

    def mouseMoveEvent(self, event):
        self.cursorPos = event.localPos()

        if self.mode == DRAWING_LINE_MODE:
            if self.isMousePressed():
                if self.mode == DRAWING_LINE_MODE:
                    self.segments[-1].setP2(self.cursorPos)

        for segment in self.segments:
            if segment.hasPoint(self.cursorPos):
                segment.setPen(Pen.active())
            else:
                segment.setPen(Pen.stable())

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawLines(painter)
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

    def enableAngleScope(self, value):
        self.mode = ANGLE_SCOPE_MODE
        self.scope = value

    def disableAngleScope(self):
        self.mode = DRAWING_LINE_MODE
        self.scope = None

    def enableLengthScope(self, value):
        self.mode = LENGTH_SCOPE_MODE
        self.scope = value

    def disableLengthScope(self):
        self.mode = DRAWING_LINE_MODE
        self.scope = None

    def enableParallelsAction(self):
        self.mode = PARALLELS_SCOPE_MODE
        self.scope = None

    def disableParallelsAction(self):
        self.mode = DRAWING_LINE_MODE
        self.scope = None

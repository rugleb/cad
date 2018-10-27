from PyQt5 import QtCore, QtGui, QtWidgets

from cad.drawing import Segment, Pen, Point


DISABLE_MODE = 0
DRAWING_LINE_MODE = 1
DRAWING_POINT_MODE = 2
ANGLE_SCOPE_MODE = 3
LENGTH_SCOPE_MODE = 4
PARALLEL_SCOPE_MODE = 5
PERPENDICULAR_SCOPE_MODE = 6
COINCIDENT_SCOPE_MODE = 7


class Sketch(QtWidgets.QWidget):

    modes = [
        DISABLE_MODE,
        DRAWING_LINE_MODE,
        DRAWING_POINT_MODE,
        ANGLE_SCOPE_MODE,
        LENGTH_SCOPE_MODE,
        PARALLEL_SCOPE_MODE,
        PERPENDICULAR_SCOPE_MODE,
        COINCIDENT_SCOPE_MODE,
    ]

    DEFAULT_MODE = DISABLE_MODE

    def __init__(self, *args):
        super().__init__(*args)

        self.memory = []

        self.points = []
        self.segments = []

        self.currentPos = None
        self.pressedPos = None

        self.constraint = None

        self.mode = self.DEFAULT_MODE
        self.scope = None

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    def setConstraint(self, constraint):
        self.constraint = constraint

    def getConstraint(self):
        return self.constraint

    def disableConstraint(self):
        self.constraint = None

    def isMousePressed(self):
        return self.pressedPos is not None

    def getCurrentPosition(self):
        return self.currentPos

    def getPressedPosition(self):
        return self.pressedPos

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            segment = self.getSelected()
            if segment:
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

        segment = self.getSelected()
        if segment is None:
            return None

        if self.mode == ANGLE_SCOPE_MODE:
            segment.setAngle(self.scope)

        if self.mode == LENGTH_SCOPE_MODE:
            segment.setLength(self.scope)

        if self.mode == PARALLEL_SCOPE_MODE:
            if self.scope is None:
                self.scope = segment
            else:
                segment.setAngle(self.scope.angle())
                self.scope = None

        if self.mode == PERPENDICULAR_SCOPE_MODE:
            if self.scope is None:
                self.scope = segment
            else:
                segment.setAngle(self.scope.angle() + 90)
                self.scope = None

        if self.mode == COINCIDENT_SCOPE_MODE:
            if self.scope is None:
                if Segment(self.currentPos, segment.p1()).length() < 6:
                    self.scope = segment.p1()
                elif Segment(self.currentPos, segment.p2()).length() < 6:
                    self.scope = segment.p2()
            else:
                if Segment(self.currentPos, segment.p1()).length() < 6:
                    segment.setP1(self.scope)
                elif Segment(self.currentPos, segment.p2()).length() < 6:
                    segment.setP2(self.scope)
                self.scope = None

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressedPos = None

        self.update()

    def mouseMoveEvent(self, event):
        self.currentPos = event.localPos()

        if self.mode == DRAWING_LINE_MODE:
            if self.isMousePressed():
                if self.mode == DRAWING_LINE_MODE:
                    self.segments[-1].setP2(self.currentPos)

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

    def setMode(self, mode):
        if mode not in self.modes:
            message = 'Given mode is invalid. Unexpected: {}'.format(mode)
            raise Exception(message)

        self.mode = mode

    def getSelected(self):
        for segment in self.segments:
            if segment.hasPoint(self.currentPos):
                return segment
        return None

    def enableDrawLineMode(self):
        self.setMode(DRAWING_LINE_MODE)

    def enableDrawPointMode(self):
        self.setMode(DRAWING_POINT_MODE)

    def enableAngleScope(self, value):
        self.setMode(ANGLE_SCOPE_MODE)
        self.scope = value

    def enableLengthScope(self, value):
        self.setMode(LENGTH_SCOPE_MODE)
        self.scope = value

    def enableParallelScope(self):
        self.setMode(PARALLEL_SCOPE_MODE)
        self.scope = None

    def enablePerpendicularScope(self):
        self.setMode(PERPENDICULAR_SCOPE_MODE)
        self.scope = None

    def enableCoincidentScope(self):
        self.setMode(COINCIDENT_SCOPE_MODE)
        self.scope = None

    def disableScope(self, mode=DEFAULT_MODE):
        self.setMode(mode)
        self.scope = None

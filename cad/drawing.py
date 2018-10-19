from PyQt5 import QtCore, QtGui


def distancePointToPoint(p1, p2):
    return Line(p1, p2).length()


def distancePointToVector(p, l):
    p1, p2 = l.p1(), l.p2()
    s = l.dy() * p.x() - l.dx() * p.y() + p2.x() * p1.y() - p2.y() * p1.x()
    return abs(s) / l.length()


def isPointOnVector(p, l):
    return distancePointToVector(p, l) == 0.


def isPointOnLine(p, l):
    if not isPointOnVector(p, l):
        return False
    return l.p1().x() <= p.x() <= l.p2().x()


class Pen:
    active = QtGui.QPen(QtCore.Qt.gray, 3, QtCore.Qt.SolidLine)
    stable = QtGui.QPen(QtCore.Qt.darkGray, 2, QtCore.Qt.SolidLine)


class Line(QtCore.QLineF):
    _pen = None

    def __init__(self, *args):
        super().__init__(*args)
        self.setPen(Pen.stable)

    def setPen(self, pen):
        if type(pen) is not QtGui.QPen:
            message = 'Invalid Pen type: expected QtGui.QPen object'
            raise Exception(message)
        self._pen = pen

    def getPen(self):
        return self._pen

    def hasPen(self):
        return isinstance(self.getPen(), QtGui.QPen)

    def hasPoint(self, point):
        d = distancePointToVector(point, self)
        return self.getPen().widthF() / 2 > d

    def hide(self):
        self.setLength(0.)


class Point(QtCore.QPointF):

    def onLine(self, line):
        return isPointOnLine(self, line)

    def onVector(self, line):
        return isPointOnVector(self, line)

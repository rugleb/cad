from PyQt5 import QtCore, QtGui


def distancePointToPoint(p1, p2):
    return Line(p1, p2).length()


def distancePointToVector(p, l):
    p1, p2 = l.p1(), l.p2()
    s = l.dy() * p.x() - l.dx() * p.y() + p2.x() * p1.y() - p2.y() * p1.x()
    return abs(s) / l.length()


class Line(QtCore.QLineF):
    _pen = None

    def setPen(self, pen):
        self._pen = pen

    def getPen(self):
        return self._pen

    def hasPen(self):
        return isinstance(self.getPen(), QtGui.QPen)


class Point(QtCore.QPointF):
    pass

from PyQt5 import QtCore, QtGui


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

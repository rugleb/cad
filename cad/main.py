import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication, QDesktopWidget

from cad.drawing import Line, Point, Pen


class Workspace(QWidget):
    _lines = None
    _point = None

    def __init__(self):
        super().__init__()

        self._lines = []
        self._point = None

        self.setMouseTracking(True)
        self.setWindowTitle('Workspace')
        self.setGeometry(QDesktopWidget().availableGeometry())
        self.show()

    def closeEvent(self, event):
        title = 'Close application'
        question = 'Are you sure you want to quit?'

        default = QMessageBox.No
        buttons = QMessageBox.No | QMessageBox.Yes

        answer = QMessageBox.question(self, title, question, buttons, default)
        if answer == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def isMousePressed(self):
        return self._point is not None

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self._point = Point(event.localPos())

    def mouseReleaseEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.LeftButton:
                point = Point(event.localPos())
                line = Line(self._point, point)
                self._point = None
                self.draw(line)

    def mouseMoveEvent(self, event):
        point = Point(event.localPos())
        if self.isMousePressed():
            if self._lines:
                self._lines.pop(-1)
            line = Line(self._point, point)
            self.draw(line)
        else:
            for line in self._lines:
                if line.hasPoint(point):
                    line.setPen(Pen.active())
                else:
                    line.setPen(Pen.stable())
            self.update()

    def draw(self, line):
        line.setPen(Pen.stable())
        self._lines.append(line)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        for line in self._lines:
            painter.setPen(line.getPen())
            painter.drawLine(line)
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    workspace = Workspace()

    sys.exit(app.exec_())

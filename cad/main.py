import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication, QDesktopWidget


def isPointOnLine(point, line):
    l1 = QtCore.QLineF(line.p1(), point)
    l2 = QtCore.QLineF(line.p2(), point)
    return line.length() == l1.length() + l2.length()


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
                self._point = event.pos()

    def mouseReleaseEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.LeftButton:
                line = QtCore.QLineF(self._point, event.pos())
                self._point = None
                self.draw(line)

    def mouseMoveEvent(self, event):
        if self.isMousePressed():
            if self._lines:
                self._lines.pop(-1)
            line = QtCore.QLineF(self._point, event.pos())
            self.draw(line)

    def draw(self, line):
        self._lines.append(line)
        self.update()

    def paintEvent(self, event):
        if self._lines:
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1))
            painter.drawLines(self._lines)
            painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    workspace = Workspace()

    sys.exit(app.exec_())

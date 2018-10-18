import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication, QDesktopWidget


class Workspace(QWidget):
    lines = None
    pressed = None

    def __init__(self):
        super().__init__()

        self.lines = []
        self.pressed = None

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
        return self.pressed is not None

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self.pressed = event.pos()

    def mouseReleaseEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.LeftButton:
                line = QtCore.QLineF(self.pressed, event.pos())
                self.pressed = None
                self.draw(line)

    def mouseMoveEvent(self, event):
        if self.isMousePressed():
            if self.lines:
                self.lines.pop(-1)
            line = QtCore.QLineF(self.pressed, event.pos())
            self.draw(line)

    def draw(self, line):
        self.lines.append(line)
        self.update()

    def paintEvent(self, event):
        if self.lines:
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            painter.drawLines(self.lines)
            painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    workspace = Workspace()

    sys.exit(app.exec_())

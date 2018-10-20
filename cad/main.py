import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication, QDesktopWidget, QMainWindow, QAction

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
        self.show()

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
            self._lines.append(line)
        for line in self._lines:
            if line.hasPoint(point):
                line.setPen(Pen.active())
            else:
                line.setPen(Pen.stable())
        self.update()

    def draw(self, line):
        self._lines.append(line)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self._drawLines(painter)
        painter.end()

    def _drawLines(self, painter):
        for line in self._lines:
            pen = line.getPen()
            painter.setPen(pen)
            painter.drawLine(line)
            width = pen.widthF()
            pen.setWidthF(width * 2)
            painter.setPen(pen)
            painter.drawPoints(line.p1(), line.p2())
            pen.setWidthF(width)


class Application(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        self._setMenuBar()
        self._setStatusBar()
        self._setGeometry()

        self.setWindowTitle('Workspace')
        self.show()

    def _setMenuBar(self):
        menu = self.menuBar()
        file = menu.addMenu('File')
        file.addAction(self._exitAction())
        file.addAction(self._openAction())
        file.addAction(self._saveAction())

    def _exitAction(self):
        action = QAction('Exit', self)
        action.setShortcut('Ctrl+Q')
        action.setStatusTip('Exit application')
        action.triggered.connect(self.close)
        return action

    def _saveAction(self):
        action = QAction('Save As', self)
        action.setShortcut('Ctrl+S')
        action.setStatusTip('Saving')
        return action

    def _openAction(self):
        action = QAction('Open', self)
        action.setShortcut('Ctrl+O')
        action.setStatusTip('Open file')
        return action

    def _setStatusBar(self):
        self.statusBar().showMessage('Ready')

    def _setGeometry(self):
        desktop = QDesktopWidget()
        self.setGeometry(desktop.availableGeometry())

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    workspace = Application()

    sys.exit(app.exec_())

from PySide2 import QtWidgets, QtGui


class Application(QtWidgets.QApplication):
    pass


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        geometry = QtGui.QScreen().geometry()
        self.setGeometry(geometry)

        self.setWindowTitle('2D CAD')
        self.statusBar().showMessage('Ready')

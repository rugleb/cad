from PyQt5.QtWidgets import *

from cad.sketch import Sketch


class Application(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        self.menu = None
        self.sketch = None
        self.drawBar = None
        self.drawBarGroup = None
        self.scopesBar = None
        self.scopesBarGroup = None

        self.initMenuBar()
        self.initStatusBar()
        self.initDrawingBar()
        self.initScopesBar()
        self.initSketch()
        self.initGeometry()

        self.setWindowTitle('Sketch')

    def initSketch(self):
        self.sketch = Sketch(self)
        self.setCentralWidget(self.sketch)

    def initMenuBar(self):
        self.menu = self.menuBar()
        file = self.menu.addMenu('File')
        file.addAction(self.exitAction())
        file.addAction(self.openAction())
        file.addAction(self.saveAction())

    def exitAction(self):
        action = QAction('Exit', self.menu)
        action.setShortcut('Ctrl+Q')
        action.setStatusTip('Exit application')
        action.triggered.connect(self.close)
        return action

    def saveAction(self):
        action = QAction('Save As', self.menu)
        action.setShortcut('Ctrl+S')
        action.setStatusTip('Saving')
        action.triggered.connect(self.showSaveDialog)
        return action

    def openAction(self):
        action = QAction('Open', self.menu)
        action.setShortcut('Ctrl+O')
        action.setStatusTip('Open file')
        action.triggered.connect(self.showOpenDialog)
        return action

    def initDrawingBar(self):
        self.drawBar = self.addToolBar('Drawing')
        self.drawBarGroup = QActionGroup(self.drawBar)

        lineAction = self.lineAction()
        pointAction = self.pointAction()

        for action in (lineAction, pointAction):
            action.setCheckable(True)
            self.drawBar.addAction(action)
            self.drawBarGroup.addAction(action)

        lineAction.setChecked(True)

    def pointAction(self):
        action = QAction('Point', self.drawBar)
        action.setShortcut('Ctrl+P')
        action.setStatusTip('Draw point')
        return action

    def lineAction(self):
        action = QAction('Line', self.drawBar)
        action.setShortcut('Ctrl+L')
        action.setStatusTip('Draw line')
        return action

    def initScopesBar(self):
        self.scopesBar = self.addToolBar('Scopes')
        self.scopesBarGroup = QActionGroup(self.scopesBar)

        actions = [
            self.angleAction(),
            self.lengthAction(),
            self.parallelsAction(),
        ]

        for action in actions:
            action.setCheckable(True)
            self.scopesBar.addAction(action)
            self.scopesBarGroup.addAction(action)

    def angleAction(self):
        action = QAction('Angle', self.scopesBar)
        action.setStatusTip('Set angle scope')
        return action

    def lengthAction(self):
        action = QAction('Length', self.scopesBar)
        action.setStatusTip('Set length scope')
        return action

    def parallelsAction(self):
        action = QAction('Parallels', self.scopesBar)
        action.setStatusTip('Set parallels scope')
        return action

    def _parallelsClickHandler(self):
        self.setStatusTip('Select line')

    def _lengthClickHandler(self):
        length, pressed = QInputDialog.getDouble(self, 'Length restriction', 'Value: ', min=0.)
        if pressed and length:
            print(length)

    def _angleClickHandler(self):
        angle, pressed = QInputDialog.getInt(self, 'Angle restriction', 'Value: ', min=-360, max=360)
        if pressed and angle:
            print(angle)

    def initStatusBar(self):
        self.statusBar().showMessage('Ready')

    def initGeometry(self):
        desktop = QDesktopWidget()
        self.setGeometry(desktop.availableGeometry())

    def showOpenDialog(self):
        files = QFileDialog.getOpenFileName(self, 'Open file', '/home', '*.json')

        if files and files[0]:
            with open(files[0], 'r') as fp:
                data = fp.read()

    def showSaveDialog(self):
        files = QFileDialog.getSaveFileName(self, 'Save As', '/home/cad.json', '*.json')

        if files and files[0]:
            with open(files[0], 'w') as fp:
                fp.write('')

    def keyPressEvent(self, QKeyEvent):
        self.sketch.keyPressEvent(QKeyEvent)

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

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from cad.sketch import Sketch


class Application(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        self.menu = None
        self.sketch = None
        self.instrumentsBar = None
        self.instrumentsBarGroup = None

        self.initSketch()
        self.initMenuBar()
        self.initStatusBar()
        self.initInstruments()
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
        action.setToolTip('Close application')
        action.setStatusTip('Close application')
        action.triggered.connect(self.close)
        return action

    def saveAction(self):
        action = QAction('Save As', self.menu)
        action.setShortcut('Ctrl+S')
        action.setToolTip('Save current application')
        action.setStatusTip('Save current application')
        action.triggered.connect(self.showSaveDialog)
        return action

    def openAction(self):
        action = QAction('Open', self.menu)
        action.setShortcut('Ctrl+O')
        action.setToolTip('Open file')
        action.setStatusTip('Open file')
        action.triggered.connect(self.showOpenDialog)
        return action

    def initInstruments(self):
        self.instrumentsBar = self.addToolBar('Drawing')
        self.instrumentsBarGroup = QActionGroup(self.instrumentsBar)

        actions = [
            self.lineAction(),
            self.pointAction(),
            self.angleAction(),
            self.lengthAction(),
            self.parallelAction(),
            self.verticalAction(),
            self.horizontalAction(),
            self.disableScopeAction(),
        ]

        for action in actions:
            action.setCheckable(True)
            action.setParent(self.instrumentsBar)
            self.instrumentsBar.addAction(action)
            self.instrumentsBarGroup.addAction(action)

    def pointAction(self):
        action = QAction('Point')
        action.setShortcut('Ctrl+P')
        action.setToolTip('Draw point')
        action.setStatusTip('Draw point')
        action.changed.connect(self.pointActionHandler)
        return action

    def pointActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableDrawPointMode()

    def lineAction(self):
        action = QAction('Segment')
        action.setShortcut('Ctrl+L')
        action.setToolTip('Draw line')
        action.setStatusTip('Draw line')
        action.changed.connect(self.lineActionHandler)
        return action

    def lineActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableDrawLineMode()

    def horizontalAction(self):
        action = QAction('Horizontal')
        action.setStatusTip('Set up horizontal scope')
        action.setToolTip('Set up horizontal scope')
        action.changed.connect(self.horizontalActionHandler)
        return action

    def horizontalActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableAngleScope(0)

    def verticalAction(self):
        action = QAction('Vertical')
        action.setStatusTip('Set up vertical scope')
        action.setToolTip('Set up vertical scope')
        action.changed.connect(self.verticalActionHandler)
        return action

    def verticalActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableAngleScope(90)

    def angleAction(self):
        action = QAction('Angle')
        action.setStatusTip('Set up angle scope')
        action.setToolTip('Set up angle scope')
        action.changed.connect(self.angleActionHandler)
        return action

    def angleActionHandler(self):
        if self.sender().isChecked():
            angle, ok = self.askAngleValue()
            if ok:
                self.sketch.enableAngleScope(angle)
            else:
                self.disableScopes()

    def askAngleValue(self):
        s1 = 'Set angle scope'
        s2 = 'Input angle value:'
        angle, ok = QInputDialog.getInt(self, s1, s2, min=-360, max=360)
        return angle, ok

    def lengthAction(self):
        action = QAction('Length')
        action.setStatusTip('Set up length scope')
        action.setToolTip('Set up length scope')
        action.changed.connect(self.lengthActionHandler)
        return action

    def lengthActionHandler(self):
        if self.sender().isChecked():
            length, ok = self.askLengthValue()
            if ok:
                self.sketch.enableLengthScope(length)
            else:
                self.disableScopes()

    def askLengthValue(self):
        s1 = 'Set length scope'
        s2 = 'Input length value:'
        length, ok = QInputDialog.getDouble(self, s1, s2, min=0)
        return length, ok

    def parallelAction(self):
        action = QAction('Parallels')
        action.setStatusTip('Set up parallels scope')
        action.setToolTip('Set up parallels scope')
        action.changed.connect(self.parallelsActionHandler)
        return action

    def parallelsActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableParallelsAction()

    def disableScopeAction(self):
        action = QAction('Disable')
        action.setStatusTip('Disable all scopes')
        action.setToolTip('Disable all scopes')
        action.triggered.connect(self.disableScopes)
        return action

    def disableScopes(self):
        for action in self.instrumentsBarGroup.actions():
            action.setChecked(False)
        self.sketch.disableScope()

    def initStatusBar(self):
        self.statusBar().showMessage('Ready')

    def initGeometry(self):
        desktop = QDesktopWidget()
        self.setGeometry(desktop.availableGeometry())

    def showOpenDialog(self):
        files = QFileDialog.getOpenFileName(self, 'Open file', '/home', '*.json')

        if files and files[0]:
            with open(files[0], 'r') as fp:
                fp.read()

    def showSaveDialog(self):
        files = QFileDialog.getSaveFileName(self, 'Save As', '/home/cad.json', '*.json')

        if files and files[0]:
            with open(files[0], 'w') as fp:
                fp.write('')

    def keyPressEvent(self, event):
        self.sketch.keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            return self.disableScopes()

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

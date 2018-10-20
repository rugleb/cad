from PyQt5.QtWidgets import *

from cad.sketch import Sketch


class Application(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        self._setMenuBar()
        self._setDrawingBar()
        self._setRestrictionsBar()
        self._setStatusBar()
        self._setGeometry()
        self._setSketch()

        self.setWindowTitle('Sketch')
        self.show()

    def _setSketch(self):
        self.sketch = Sketch(self)
        self.setCentralWidget(self.sketch)

    def _setMenuBar(self):
        file = self.menuBar().addMenu('File')
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
        action.triggered.connect(self._showSaveDialog)
        return action

    def _openAction(self):
        action = QAction('Open', self)
        action.setShortcut('Ctrl+O')
        action.setStatusTip('Open file')
        action.triggered.connect(self._showOpenDialog)
        return action

    def _setDrawingBar(self):
        toolbar = self.addToolBar('Drawing')

        self.pointButton = QPushButton('Point', toolbar)
        self.segmentButton = QPushButton('Segment', toolbar)

        self.pointButton.clicked.connect(self._handlePointClick)
        self.segmentButton.clicked.connect(self._handleSegmentClick)

        toolbar.addWidget(QLabel('Drawing ', toolbar))
        toolbar.addWidget(self.pointButton)
        toolbar.addWidget(self.segmentButton)

    def _setRestrictionsBar(self):
        self._restrictionBar = self.addToolBar('Restrictions')

        self._restrictionBar.addWidget(QLabel('Restrictions: '))
        self._setAngleRestriction()

    def _setAngleRestriction(self):
        self._angleButton = QPushButton('Angle')
        self._angleButton.clicked.connect(self._angleClickHandler)

        self._angleButton.setParent(self._restrictionBar)
        self._restrictionBar.addWidget(self._angleButton)

    def _angleClickHandler(self):
        angle, pressed = QInputDialog.getInt(self, 'Angle restriction', 'Value: ', min=-360, max=360)
        if pressed and angle:
            print(angle)

    def _handlePointClick(self):
        self.segmentButton.setDown(False)
        self.pointButton.setDown(not self.pointButton.isDown())

    def _handleSegmentClick(self):
        self.pointButton.setDown(False)
        self.segmentButton.setDown(not self.segmentButton.isDown())

    def _setStatusBar(self):
        self.statusBar().showMessage('Ready')

    def _setGeometry(self):
        desktop = QDesktopWidget()
        self.setGeometry(desktop.availableGeometry())

    def _showOpenDialog(self):
        files = QFileDialog.getOpenFileName(self, 'Open file', '/home', '*.json')

        if files and files[0]:
            with open(files[0], 'r') as fp:
                data = fp.read()

    def _showSaveDialog(self):
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

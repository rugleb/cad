from PyQt5.QtWidgets import QMainWindow, \
    QDesktopWidget, QMessageBox, QFileDialog, QAction


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
        action.triggered.connect(self._showSaveDialog)
        return action

    def _openAction(self):
        action = QAction('Open', self)
        action.setShortcut('Ctrl+O')
        action.setStatusTip('Open file')
        action.triggered.connect(self._showOpenDialog)
        return action

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

    def _showSaveDialog(self):
        files = QFileDialog.getSaveFileName(self, 'Save As', '/home/cad.json', '*.json')

        with open(files[0], 'w') as fp:
            fp.write('')

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

from PySide2 import QtWidgets, QtGui

from cad.logging import logger


class Application(QtWidgets.QApplication):
    pass


class Action(QtWidgets.QAction):
    pass


class Menu(QtWidgets.QMenu):
    pass


class MenuBar(QtWidgets.QMenuBar):
    pass


class KeySequence(QtGui.QKeySequence):
    pass


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.logger = logger

        self.setMenuBar(self.makeMenuBar())

        geometry = QtGui.QScreen().geometry()
        self.setGeometry(geometry)

        self.setWindowTitle('2D CAD')
        self.statusBar().showMessage('Ready')

    def makeMenuBar(self) -> MenuBar:
        bar = MenuBar(self)
        bar.addMenu(self.makeFileMenu(bar))
        bar.addMenu(self.makeEditMenu(bar))
        return bar

    def makeFileMenu(self, bar: MenuBar) -> Menu:
        menu = Menu('&File', bar)
        menu.addAction(self.makeOpenAction(menu))
        menu.addAction(self.makeSaveAction(menu))
        menu.addSeparator()
        menu.addAction(self.makeQuitAction(menu))
        return menu

    def makeEditMenu(self, bar: MenuBar) -> Menu:
        menu = Menu('&Edit', bar)
        menu.addAction(self.makeUndoAction(menu))
        menu.addAction(self.makeRedoAction(menu))
        menu.addSeparator()
        menu.addAction(self.makeCutAction(menu))
        menu.addAction(self.makeCopyAction(menu))
        menu.addAction(self.makePasteAction(menu))
        menu.addAction(self.makeDeleteAction(menu))
        return menu

    def makeOpenAction(self, menu: Menu) -> Action:
        action = Action('Save', menu)
        action.setShortcut(KeySequence('Ctrl+O'))
        action.setToolTip('Open new file')
        action.triggered.connect(self.open)
        return action

    def makeSaveAction(self, menu: Menu) -> Action:
        action = Action('Save', menu)
        action.setShortcut(KeySequence('Ctrl+S'))
        action.setToolTip('Save file')
        action.triggered.connect(self.save)
        return action

    def makeQuitAction(self, menu: Menu) -> Action:
        action = Action('Quit', menu)
        action.setShortcut(KeySequence('Ctrl+Q'))
        action.setToolTip('Close application')
        action.triggered.connect(self.close)
        return action

    def makeUndoAction(self, menu: Menu) -> Action:
        action = Action('Undo', menu)
        action.setShortcut(KeySequence('Ctrl+Z'))
        action.setToolTip('Undo previous action')
        action.triggered.connect(self.undo)
        return action

    def makeRedoAction(self, menu: Menu) -> Action:
        action = Action('Redo', menu)
        action.setShortcut(KeySequence('Ctrl+Shift+Z'))
        action.setToolTip('Redo previous action')
        action.triggered.connect(self.redo)
        return action

    def makeCutAction(self, menu: Menu) -> Action:
        action = Action('Cut', menu)
        action.setShortcut(KeySequence('Ctrl+X'))
        action.setToolTip('Cut selected object')
        action.triggered.connect(self.cut)
        return action

    def makeCopyAction(self, menu: Menu) -> Action:
        action = Action('Copy', menu)
        action.setShortcut(KeySequence('Ctrl+C'))
        action.setToolTip('Copy selected object')
        action.triggered.connect(self.redo)
        return action

    def makePasteAction(self, menu: Menu) -> Action:
        action = Action('Paste', menu)
        action.setShortcut(KeySequence('Ctrl+V'))
        action.setToolTip('Paste object from buffer')
        action.triggered.connect(self.paste)
        return action

    def makeDeleteAction(self, menu: Menu) -> Action:
        action = Action('Delete', menu)
        action.setShortcut(KeySequence('Delete'))
        action.setToolTip('Delete selected object')
        action.triggered.connect(self.delete)
        return action

    def open(self) -> None:
        self.logger.debug('Open action triggered')

    def save(self) -> None:
        self.logger.debug('Save action triggered')

    def undo(self) -> None:
        self.logger.debug('Undo action triggered')

    def redo(self) -> None:
        self.logger.debug('Redo action triggered')

    def copy(self) -> None:
        self.logger.debug('Copy action triggered')

    def cut(self) -> None:
        self.logger.debug('Cut action triggered')

    def paste(self) -> None:
        self.logger.debug('Paste action triggered')

    def delete(self) -> None:
        self.logger.debug('Delete action triggered')

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        pass

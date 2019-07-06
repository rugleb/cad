import os
from PySide2 import QtWidgets, QtGui

from cad.logging import logger


def iconPath(name: str) -> str:
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'icons', name)


class Application(QtWidgets.QApplication):
    pass


class Action(QtWidgets.QAction):
    pass


class Menu(QtWidgets.QMenu):
    pass


class MenuBar(QtWidgets.QMenuBar):
    pass


class ToolBar(QtWidgets.QToolBar):
    pass


class Icon(QtGui.QIcon):
    pass


class ActionGroup(QtWidgets.QActionGroup):
    pass


class KeySequence(QtGui.QKeySequence):
    pass


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.logger = logger

        drawBar, drawBarGroup = self.makeDrawBar()
        self.addToolBar(drawBar)

        menuBar = self.makeMenuBar()
        self.setMenuBar(menuBar)

        geometry = QtGui.QScreen().geometry()
        self.setGeometry(geometry)

        self.setWindowTitle('2D CAD')
        self.statusBar().showMessage('Ready')

    def makeDrawBar(self) -> (ToolBar, ActionGroup):
        bar = ToolBar('Draw toolbar', self)
        group = self.makeDrawBarGroup(bar)
        actions = group.actions()
        bar.addActions(actions)
        before = actions[2]
        bar.insertSeparator(before)
        return bar, group

    def makeDrawBarGroup(self, bar: ToolBar) -> ActionGroup:
        group = ActionGroup(self)
        group.addAction(self.makePointAction(bar))
        group.addAction(self.makeLineAction(bar))
        group.addAction(self.makeParallelAction(bar))
        group.addAction(self.makePerpendicularAction(bar))
        group.addAction(self.makeCoincidentAction(bar))
        group.addAction(self.makeFixedAction(bar))
        group.addAction(self.makeAngleAction(bar))
        group.addAction(self.makeVerticalAction(bar))
        group.addAction(self.makeHorizontalAction(bar))
        return group

    def makePointAction(self, bar: ToolBar) -> Action:
        action = Action('Point drawing', bar)
        action.setShortcut(KeySequence('Ctrl+P'))
        action.setStatusTip('Enable point drawing mode')
        action.setIcon(Icon(iconPath('point.png')))
        action.setCheckable(True)
        action.triggered.connect(self.point)
        return action

    def makeLineAction(self, bar) -> Action:
        action = Action('Line drawing', bar)
        action.setShortcut(KeySequence('Ctrl+L'))
        action.setStatusTip('Enable line drawing mode')
        action.setIcon(Icon(iconPath('line.png')))
        action.setCheckable(True)
        action.triggered.connect(self.line)
        return action

    def makeParallelAction(self, bar: ToolBar) -> Action:
        action = Action('Parallel constraint', bar)
        action.setStatusTip('Enable parallel constraint')
        action.setIcon(Icon(iconPath('parallel.png')))
        action.setCheckable(True)
        action.triggered.connect(self.parallel)
        return action

    def makePerpendicularAction(self, bar: ToolBar) -> Action:
        action = Action('Perpendicular constraint', bar)
        action.setStatusTip('Enable perpendicular constraint')
        action.setIcon(Icon(iconPath('perpendicular.png')))
        action.setCheckable(True)
        action.triggered.connect(self.perpendicular)
        return action

    def makeCoincidentAction(self, bar: ToolBar) -> Action:
        action = Action('Coincident constraint', bar)
        action.setStatusTip('Enable coincident constraint')
        action.setIcon(Icon(iconPath('coincident.png')))
        action.setCheckable(True)
        action.triggered.connect(self.coincident)
        return action

    def makeFixedAction(self, bar: ToolBar) -> Action:
        action = Action('Fixed constraint', bar)
        action.setStatusTip('Enable fixed constraint')
        action.setIcon(Icon(iconPath('fixed.png')))
        action.setCheckable(True)
        action.triggered.connect(self.fixed)
        return action

    def makeAngleAction(self, bar: ToolBar) -> Action:
        action = Action('Angle constraint', bar)
        action.setStatusTip('Enable angle constraint')
        action.setIcon(Icon(iconPath('angle.png')))
        action.setCheckable(True)
        action.triggered.connect(self.angle)
        return action

    def makeVerticalAction(self, bar: ToolBar) -> Action:
        action = Action('Vertical constraint', bar)
        action.setStatusTip('Enable vertical constraint')
        action.setIcon(Icon(iconPath('vertical.png')))
        action.setCheckable(True)
        action.triggered.connect(self.vertical)
        return action

    def makeHorizontalAction(self, bar: ToolBar) -> Action:
        action = Action('Horizontal constraint', bar)
        action.setStatusTip('Enable horizontal constraint')
        action.setIcon(Icon(iconPath('horizontal.png')))
        action.setCheckable(True)
        action.triggered.connect(self.horizontal)
        return action

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

    def point(self) -> None:
        self.logger.debug('Point action triggered')

    def line(self) -> None:
        self.logger.debug('Line action triggered')

    def parallel(self) -> None:
        self.logger.debug('Parallel action triggered')

    def perpendicular(self) -> None:
        self.logger.debug('Perpendicular action triggered')

    def coincident(self) -> None:
        self.logger.debug('Coincident action triggered')

    def fixed(self) -> None:
        self.logger.debug('Fixed action triggered')

    def angle(self) -> None:
        self.logger.debug('Angle action triggered')

    def vertical(self) -> None:
        self.logger.debug('Vertical action triggered')

    def horizontal(self) -> None:
        self.logger.debug('Horizontal action triggered')

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        pass

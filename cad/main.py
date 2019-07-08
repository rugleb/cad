import os
from PySide2 import QtWidgets, QtGui, QtCore

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


class Icon(QtGui.QIcon):
    pass


class ActionGroup(QtWidgets.QActionGroup):

    def addActions(self, actions: iter) -> None:
        for action in actions:
            self.addAction(action)


class ToolBar(QtWidgets.QToolBar):

    def toActionGroup(self) -> ActionGroup:
        group = ActionGroup(self)
        group.addActions(self.actions())
        return group


class KeySequence(QtGui.QKeySequence):
    pass


class MessageBox(QtWidgets.QMessageBox):
    pass


class FileDialog(QtWidgets.QFileDialog):
    pass


class MainWindow(QtWidgets.QMainWindow):
    width = 800
    height = 500

    def __init__(self):
        super().__init__()

        self.logger = logger

        self.board: DrawingBoard = self.makeDrawingBoard()
        self.setCentralWidget(self.board)

        self.addToolBar(self.makeDrawBar())

        self.setMenuBar(self.makeMenuBar())
        self.setGeometry(self.getGeometry())

        self.setWindowTitle('2D CAD')
        self.statusBar().showMessage('Ready')

    def makeDrawingBoard(self) -> QtWidgets.QWidget:
        board = DrawingBoard(self)
        board.mouseMoved.connect(self.mouseMovedHandler)
        return board

    def getGeometry(self) -> QtCore.QRect:
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        x = (screen.width() - self.width) / 2
        y = (screen.height() - self.height) / 2
        rect = QtCore.QRectF(x, y, self.width, self.height)
        return rect.toRect()

    def makeDrawBar(self) -> ToolBar:
        bar = ToolBar('Draw toolbar', self)
        bar.setIconSize(QtCore.QSize(40, 40))
        bar.addAction(self.makeDisableAction(bar))
        bar.addSeparator()
        bar.addAction(self.makePointAction(bar))
        bar.addAction(self.makeLineAction(bar))
        bar.addSeparator()
        bar.addAction(self.makeParallelAction(bar))
        bar.addAction(self.makePerpendicularAction(bar))
        bar.addAction(self.makeCoincidentAction(bar))
        bar.addAction(self.makeFixedAction(bar))
        bar.addAction(self.makeAngleAction(bar))
        bar.addAction(self.makeVerticalAction(bar))
        bar.addAction(self.makeHorizontalAction(bar))
        bar.toActionGroup()
        return bar

    def makeDisableAction(self, bar: ToolBar) -> Action:
        action = Action('Disable', bar)
        action.setShortcut(KeySequence('Escape'))
        action.setStatusTip('Disable draw')
        action.setIcon(Icon(iconPath('cursor.png')))
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.disable)
        return action

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
        bar.addMenu(self.makeViewMenu(bar))
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

    def makeViewMenu(self, bar: MenuBar) -> Menu:
        menu = Menu('&View', bar)
        menu.addAction(self.makeMaxScreenAction(menu))
        menu.addAction(self.makeNormalScreenAction(menu))
        return menu

    def makeOpenAction(self, menu: Menu) -> Action:
        action = Action('Save', menu)
        action.setShortcut(KeySequence('Ctrl+O'))
        action.setStatusTip('Open new file')
        action.triggered.connect(self.open)
        return action

    def makeSaveAction(self, menu: Menu) -> Action:
        action = Action('Save', menu)
        action.setShortcut(KeySequence('Ctrl+S'))
        action.setStatusTip('Save file')
        action.triggered.connect(self.save)
        return action

    def makeQuitAction(self, menu: Menu) -> Action:
        action = Action('Quit', menu)
        action.setShortcut(KeySequence('Ctrl+Q'))
        action.setStatusTip('Close application')
        action.triggered.connect(self.close)
        return action

    def makeUndoAction(self, menu: Menu) -> Action:
        action = Action('Undo', menu)
        action.setShortcut(KeySequence('Ctrl+Z'))
        action.setStatusTip('Undo previous action')
        action.triggered.connect(self.undo)
        return action

    def makeRedoAction(self, menu: Menu) -> Action:
        action = Action('Redo', menu)
        action.setShortcut(KeySequence('Ctrl+Shift+Z'))
        action.setStatusTip('Redo previous action')
        action.triggered.connect(self.redo)
        return action

    def makeCutAction(self, menu: Menu) -> Action:
        action = Action('Cut', menu)
        action.setShortcut(KeySequence('Ctrl+X'))
        action.setStatusTip('Cut selected object')
        action.triggered.connect(self.cut)
        return action

    def makeCopyAction(self, menu: Menu) -> Action:
        action = Action('Copy', menu)
        action.setShortcut(KeySequence('Ctrl+C'))
        action.setStatusTip('Copy selected object')
        action.triggered.connect(self.redo)
        return action

    def makePasteAction(self, menu: Menu) -> Action:
        action = Action('Paste', menu)
        action.setShortcut(KeySequence('Ctrl+V'))
        action.setStatusTip('Paste object from buffer')
        action.triggered.connect(self.paste)
        return action

    def makeDeleteAction(self, menu: Menu) -> Action:
        action = Action('Delete', menu)
        action.setShortcut(KeySequence('Delete'))
        action.setStatusTip('Delete selected object')
        action.triggered.connect(self.delete)
        return action

    def makeMaxScreenAction(self, menu: Menu) -> Action:
        action = Action('Max Screen', menu)
        action.setShortcut(KeySequence('F10'))
        action.setStatusTip('Shows the window as maximized')
        action.triggered.connect(self.showMaximized)
        return action

    def makeNormalScreenAction(self, menu: Menu) -> Action:
        action = Action('Normal Screen', menu)
        action.setShortcut(KeySequence('F9'))
        action.setStatusTip('Shows the window as normal')
        action.triggered.connect(self.showNormal)
        return action

    def open(self) -> None:
        title = 'Open file'
        options = FileDialog.DontUseNativeDialog

        file, _ = FileDialog.getOpenFileName(self, title, '.', options=options)
        if file:
            pass

    def save(self) -> None:
        title = 'Save file'
        options = FileDialog.DontUseNativeDialog

        file, _ = FileDialog.getSaveFileName(self, title, '.', options=options)
        if file:
            pass

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

    def disable(self) -> None:
        handler = NullHandler(self.board)
        self.board.setHandler(handler)

    def point(self) -> None:
        handler = PointHandler(self.board)
        self.board.setHandler(handler)

    def line(self) -> None:
        handler = LineHandler(self.board)
        self.board.setHandler(handler)

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
        ask = 'Are you sure you want to quit?'
        title = 'Close application'
        yes, no = MessageBox.Yes, MessageBox.No

        if MessageBox.question(self, title, ask, yes | no) == yes:
            event.accept()
        else:
            event.ignore()

    def mouseMovedHandler(self, event: QtGui.QMouseEvent) -> None:
        x, y = event.x(), event.y()
        message = f'x: {x}, y: {y}'
        self.statusBar().showMessage(message)


class NullHandler(QtCore.QObject):

    def __init__(self, board: QtWidgets.QWidget):
        super().__init__()

        self.board: DrawingBoard = board

    def onMouseMoved(self, event: QtGui.QMouseEvent):
        pass

    def onMousePressed(self, event: QtGui.QMouseEvent):
        pass


class PointHandler(NullHandler):

    def onMousePressed(self, event: QtGui.QMouseEvent):
        self.board.addPoint(event.localPos())
        self.board.repaint()


class LineHandler(NullHandler):

    def __init__(self, board: QtWidgets.QWidget):
        super().__init__(board)

        self.p1 = None

    def onMouseMoved(self, event: QtGui.QMouseEvent):
        if self.p1:
            p2 = event.localPos()
            self.board.lines[-1].setP2(p2)
            self.board.repaint()

    def onMousePressed(self, event: QtGui.QMouseEvent):
        if self.p1 is None:
            self.p1 = event.localPos()

            line = QtCore.QLineF(self.p1, self.p1)
            self.board.addLine(line)

        else:
            self.p1 = None


class Painter(QtGui.QPainter):

    def drawCircle(self, center: QtCore.QPointF, radius: int) -> None:
        self.drawEllipse(center, radius, radius)

    def drawCircles(self, centers: list, radius: int) -> None:
        self.drawEllipses(centers, radius, radius)

    def drawEllipses(self, centers: list, rx: int, ry: int) -> None:
        for center in centers:
            self.drawEllipse(center, rx, ry)


class DrawingBoard(QtWidgets.QWidget):
    mouseMoved = QtCore.Signal(QtGui.QMouseEvent)
    mousePressed = QtCore.Signal(QtGui.QMouseEvent)

    def __init__(self, parent: MainWindow):
        super().__init__(parent)

        self.handler = NullHandler(self)

        self.lines = []
        self.points = []

        self.setMouseTracking(True)

    def addPoint(self, point: QtCore.QPointF):
        self.points.append(point)

    def addLine(self, line: QtCore.QLineF):
        self.lines.append(line)

    def setHandler(self, handler: NullHandler):
        self.handler = handler

        self.mouseMoved.connect(self.handler.onMouseMoved)
        self.mousePressed.connect(self.handler.onMousePressed)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = Painter()
        painter.begin(self)
        color, radius = QtGui.QColor(54, 93, 171), 6
        self.drawPoints(painter, radius, color)
        self.drawLines(painter, radius, color)
        painter.end()

    def drawPoints(self, painter: Painter, radius: int, color: QtGui.QColor):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(color)
        painter.setRenderHint(painter.Antialiasing, True)
        painter.drawCircles(self.points, radius)

    def drawLines(self, painter: Painter, radius: int, color: QtGui.QColor):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(color)
        painter.setRenderHint(painter.Antialiasing, True)

        for line in self.lines:
            painter.drawCircle(line.p1(), radius)
            painter.drawCircle(line.p2(), radius)

        painter.setPen(QtGui.QPen(color, 3, QtCore.Qt.SolidLine))
        painter.drawLines(self.lines)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.mouseMoved.emit(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.mousePressed.emit(event)

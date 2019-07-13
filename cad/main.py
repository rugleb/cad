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
        self.fileName = None

        self.board: DrawingBoard = self.createDrawingBoard()
        self.setCentralWidget(self.board)

        self.addToolBar(self.createDrawBar())

        self.setMenuBar(self.createMenuBar())
        self.setGeometry(self.getGeometry())

        self.updateWindowTitle()
        self.statusBar().showMessage('Ready')

    def createDrawingBoard(self) -> QtWidgets.QWidget:
        board = DrawingBoard(self)
        board.mouseMoved.connect(self.mouseMovedHandler)
        return board

    def getGeometry(self) -> QtCore.QRect:
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        x = (screen.width() - self.width) / 2
        y = (screen.height() - self.height) / 2
        rect = QtCore.QRectF(x, y, self.width, self.height)
        return rect.toRect()

    def createDrawBar(self) -> ToolBar:
        bar = ToolBar(self)
        bar.setIconSize(QtCore.QSize(40, 40))
        bar.addAction(self.createCancelAction(bar))
        bar.addSeparator()
        bar.addAction(self.createPointAction(bar))
        bar.addAction(self.createLineAction(bar))
        bar.addSeparator()
        bar.addAction(self.createParallelAction(bar))
        bar.addAction(self.createPerpendicularAction(bar))
        bar.addAction(self.createCoincidentAction(bar))
        bar.addAction(self.createFixedAction(bar))
        bar.addAction(self.createAngleAction(bar))
        bar.addAction(self.createVerticalAction(bar))
        bar.addAction(self.createHorizontalAction(bar))
        bar.toActionGroup()
        return bar

    def createCancelAction(self, bar: ToolBar) -> Action:
        action = Action('Cancel', bar)
        action.setShortcut(KeySequence.Cancel)
        action.setStatusTip('Cancel drawing')
        action.setIcon(Icon(iconPath('cursor.png')))
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.cancel)
        return action

    def createPointAction(self, bar: ToolBar) -> Action:
        action = Action('Point drawing', bar)
        action.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_P)
        action.setStatusTip('Enable point drawing mode')
        action.setIcon(Icon(iconPath('point.png')))
        action.setCheckable(True)
        action.triggered.connect(self.point)
        return action

    def createLineAction(self, bar) -> Action:
        action = Action('Line drawing', bar)
        action.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        action.setStatusTip('Enable line drawing mode')
        action.setIcon(Icon(iconPath('line.png')))
        action.setCheckable(True)
        action.triggered.connect(self.line)
        return action

    def createParallelAction(self, bar: ToolBar) -> Action:
        action = Action('Parallel constraint', bar)
        action.setStatusTip('Enable parallel constraint')
        action.setIcon(Icon(iconPath('parallel.png')))
        action.setCheckable(True)
        action.triggered.connect(self.parallel)
        return action

    def createPerpendicularAction(self, bar: ToolBar) -> Action:
        action = Action('Perpendicular constraint', bar)
        action.setStatusTip('Enable perpendicular constraint')
        action.setIcon(Icon(iconPath('perpendicular.png')))
        action.setCheckable(True)
        action.triggered.connect(self.perpendicular)
        return action

    def createCoincidentAction(self, bar: ToolBar) -> Action:
        action = Action('Coincident constraint', bar)
        action.setStatusTip('Enable coincident constraint')
        action.setIcon(Icon(iconPath('coincident.png')))
        action.setCheckable(True)
        action.triggered.connect(self.coincident)
        return action

    def createFixedAction(self, bar: ToolBar) -> Action:
        action = Action('Fixed constraint', bar)
        action.setStatusTip('Enable fixed constraint')
        action.setIcon(Icon(iconPath('fixed.png')))
        action.setCheckable(True)
        action.triggered.connect(self.fixed)
        return action

    def createAngleAction(self, bar: ToolBar) -> Action:
        action = Action('Angle constraint', bar)
        action.setStatusTip('Enable angle constraint')
        action.setIcon(Icon(iconPath('angle.png')))
        action.setCheckable(True)
        action.triggered.connect(self.angle)
        return action

    def createVerticalAction(self, bar: ToolBar) -> Action:
        action = Action('Vertical constraint', bar)
        action.setStatusTip('Enable vertical constraint')
        action.setIcon(Icon(iconPath('vertical.png')))
        action.setCheckable(True)
        action.triggered.connect(self.vertical)
        return action

    def createHorizontalAction(self, bar: ToolBar) -> Action:
        action = Action('Horizontal constraint', bar)
        action.setStatusTip('Enable horizontal constraint')
        action.setIcon(Icon(iconPath('horizontal.png')))
        action.setCheckable(True)
        action.triggered.connect(self.horizontal)
        return action

    def createMenuBar(self) -> MenuBar:
        bar = MenuBar(self)
        bar.addMenu(self.createFileMenu(bar))
        bar.addMenu(self.createEditMenu(bar))
        bar.addMenu(self.createViewMenu(bar))
        return bar

    def createFileMenu(self, bar: MenuBar) -> Menu:
        menu = Menu('&File', bar)
        menu.addAction(self.createOpenAction(menu))
        menu.addAction(self.createSaveAction(menu))
        menu.addAction(self.createSaveAsAction(menu))
        menu.addSeparator()
        menu.addAction(self.createQuitAction(menu))
        return menu

    def createEditMenu(self, bar: MenuBar) -> Menu:
        menu = Menu('&Edit', bar)
        menu.addAction(self.createUndoAction(menu))
        menu.addAction(self.createRedoAction(menu))
        menu.addSeparator()
        menu.addAction(self.createCutAction(menu))
        menu.addAction(self.createCopyAction(menu))
        menu.addAction(self.createPasteAction(menu))
        menu.addAction(self.createDeleteAction(menu))
        return menu

    def createViewMenu(self, bar: MenuBar) -> Menu:
        menu = Menu('&View', bar)
        menu.addAction(self.createMaxScreenAction(menu))
        menu.addAction(self.createNormalScreenAction(menu))
        return menu

    def createOpenAction(self, menu: Menu) -> Action:
        action = Action('Open', menu)
        action.setShortcut(KeySequence.Open)
        action.setStatusTip('Open file')
        action.triggered.connect(self.open)
        return action

    def createSaveAction(self, menu: Menu) -> Action:
        action = Action('Save', menu)
        action.setShortcut(KeySequence.Save)
        action.setStatusTip('Save')
        action.triggered.connect(self.save)
        return action

    def createSaveAsAction(self, menu: Menu) -> Action:
        action = Action('Save', menu)
        action.setShortcut(KeySequence.SaveAs)
        action.setStatusTip('Save as')
        action.triggered.connect(self.saveAs)
        return action

    def createQuitAction(self, menu: Menu) -> Action:
        action = Action('Quit', menu)
        action.setShortcut(KeySequence.Quit)
        action.setStatusTip('Close application')
        action.triggered.connect(self.close)
        return action

    def createUndoAction(self, menu: Menu) -> Action:
        action = Action('Undo', menu)
        action.setShortcut(KeySequence.Undo)
        action.setStatusTip('Undo previous action')
        action.triggered.connect(self.undo)
        return action

    def createRedoAction(self, menu: Menu) -> Action:
        action = Action('Redo', menu)
        action.setShortcut(KeySequence.Redo)
        action.setStatusTip('Redo previous action')
        action.triggered.connect(self.redo)
        return action

    def createCutAction(self, menu: Menu) -> Action:
        action = Action('Cut', menu)
        action.setShortcut(KeySequence.Cut)
        action.setStatusTip('Cut selected object')
        action.triggered.connect(self.cut)
        return action

    def createCopyAction(self, menu: Menu) -> Action:
        action = Action('Copy', menu)
        action.setShortcut(KeySequence.Copy)
        action.setStatusTip('Copy selected object')
        action.triggered.connect(self.redo)
        return action

    def createPasteAction(self, menu: Menu) -> Action:
        action = Action('Paste', menu)
        action.setShortcut(KeySequence.Paste)
        action.setStatusTip('Paste object from buffer')
        action.triggered.connect(self.paste)
        return action

    def createDeleteAction(self, menu: Menu) -> Action:
        action = Action('Delete', menu)
        action.setShortcut(KeySequence.Delete)
        action.setStatusTip('Delete selected object')
        action.triggered.connect(self.delete)
        return action

    def createMaxScreenAction(self, menu: Menu) -> Action:
        action = Action('Max Screen', menu)
        action.setShortcut(KeySequence('F10'))
        action.setStatusTip('Shows the window as maximized')
        action.triggered.connect(self.showMaximized)
        return action

    def createNormalScreenAction(self, menu: Menu) -> Action:
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

    def hasFile(self) -> bool:
        return self.fileName is not None

    def setFileName(self, name: str) -> None:
        self.fileName = name

    def save(self) -> None:
        if not self.hasFile():
            return self.saveAs()
        return self.dump()

    def saveAs(self) -> None:
        title = 'Save file as'
        options = FileDialog.DontUseNativeDialog

        file, _ = FileDialog.getSaveFileName(self, title, '.', options=options)
        if file:
            self.setFileName(file)
            self.updateWindowTitle()
            self.dump()

    def dump(self) -> None:
        with open(self.fileName, 'w') as f:
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

    def cancel(self) -> None:
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

        accepted = MessageBox.question(self, title, ask, yes | no) == yes
        event.setAccepted(accepted)

    def mouseMovedHandler(self, event: QtGui.QMouseEvent) -> None:
        x, y = event.x(), event.y()
        message = f'x: {x}, y: {y}'
        self.statusBar().showMessage(message)

    def updateWindowTitle(self) -> None:
        fileName = self.fileName or 'Untitled'
        title = f'CAD 2D - {fileName}'
        self.setWindowTitle(title)


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
        self.drawLines(painter, color)
        painter.end()

    def drawPoints(self, painter: Painter, radius: int, color: QtGui.QColor):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(color)
        painter.setRenderHint(painter.Antialiasing, True)
        painter.drawCircles(self.points, radius)
        for line in self.lines:
            painter.drawCircle(line.p1(), radius)
            painter.drawCircle(line.p2(), radius)

    def drawLines(self, painter: Painter, color: QtGui.QColor):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(color)
        painter.setRenderHint(painter.Antialiasing, True)
        painter.setPen(QtGui.QPen(color, 3, QtCore.Qt.SolidLine))
        painter.drawLines(self.lines)

        # color = QtGui.QColor(254,  137, 144)    # active color

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.mouseMoved.emit(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.mousePressed.emit(event)

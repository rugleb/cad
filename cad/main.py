from __future__ import annotations

import os
from typing import List
from PySide2 import QtWidgets, QtGui, QtCore

from cad.logging import logger


Point = QtCore.QPointF
Segment = QtCore.QLineF


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

    fileNameChanged = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

        self.logger = logger

        self.fileName: str = ''

        self.sketch = self.createSketch()
        self.setCentralWidget(self.sketch)

        self.addToolBar(self.createDrawBar())

        self.setMenuBar(self.createMenuBar())
        self.setGeometry(self.getGeometry())

        self.updateWindowTitle()
        self.statusBar().showMessage('Ready')

        self.fileNameChanged.connect(self.updateWindowTitle)

    def createSketch(self) -> Sketch:
        sketch = Sketch(self)
        sketch.mouseMoved.connect(self.updateStatusBar)
        return sketch

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
        action.setShortcut(QtCore.Qt.ShiftModifier + QtCore.Qt.Key_F10)
        action.setStatusTip('Shows the window as maximized')
        action.triggered.connect(self.showMaximized)
        return action

    def createNormalScreenAction(self, menu: Menu) -> Action:
        action = Action('Normal Screen', menu)
        action.setShortcut(QtCore.Qt.ShiftModifier + QtCore.Qt.Key_F9)
        action.setStatusTip('Shows the window as normal')
        action.triggered.connect(self.showNormal)
        return action

    def open(self) -> None:
        title = 'Open file'
        options = FileDialog.DontUseNativeDialog

        file, _ = FileDialog.getOpenFileName(self, title, '.', options=options)
        if file:
            self.setFileName(file)
            self.load()

    def hasFile(self) -> bool:
        return bool(self.fileName)

    def setFileName(self, name: str) -> None:
        if name != self.fileName:
            self.fileName = name
            self.fileNameChanged.emit(name)

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
            self.dump()

    def dump(self) -> None:
        with open(self.fileName, 'w'):
            pass

    def load(self) -> None:
        with open(self.fileName, 'r'):
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
        self.logger.debug('Cancel action triggered')

        controller = CancelController(self.sketch)
        self.sketch.setController(controller)

    def point(self) -> None:
        self.logger.debug('Point action triggered')

        controller = PointController(self.sketch)
        self.sketch.setController(controller)

    def line(self) -> None:
        self.logger.debug('Line action triggered')

        controller = LineController(self.sketch)
        self.sketch.setController(controller)

    def parallel(self) -> None:
        self.logger.debug('Parallel action triggered')

        controller = ParallelController(self.sketch)
        self.sketch.setController(controller)

    def perpendicular(self) -> None:
        self.logger.debug('Perpendicular action triggered')

        controller = PerpendicularController(self.sketch)
        self.sketch.setController(controller)

    def coincident(self) -> None:
        self.logger.debug('Coincident action triggered')

        controller = CoincidentController(self.sketch)
        self.sketch.setController(controller)

    def fixed(self) -> None:
        self.logger.debug('Fixed action triggered')

        controller = FixedController(self.sketch)
        self.sketch.setController(controller)

    def angle(self) -> None:
        self.logger.debug('Angle action triggered')

        controller = AngleController(self.sketch)
        self.sketch.setController(controller)

    def vertical(self) -> None:
        self.logger.debug('Vertical action triggered')

        controller = VerticalController(self.sketch)
        self.sketch.setController(controller)

    def horizontal(self) -> None:
        self.logger.debug('Horizontal action triggered')

        controller = HorizontalController(self.sketch)
        self.sketch.setController(controller)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        ask = 'Are you sure you want to quit?'
        title = 'Close application'
        yes, no = MessageBox.Yes, MessageBox.No

        accepted = MessageBox.question(self, title, ask, yes | no) == yes
        event.setAccepted(accepted)

    def updateWindowTitle(self) -> None:
        file = self.fileName or 'Untitled'
        title = f'CAD 2D - {file}'
        self.setWindowTitle(title)

    def updateStatusBar(self, p: QtCore.QPointF) -> None:
        x, y = p.x(), p.y()
        message = f'x: {x}, y: {y}'
        self.statusBar().showMessage(message)


class Sketch(QtWidgets.QWidget):
    mouseMoved = QtCore.Signal(Point)
    mousePressed = QtCore.Signal(Point)

    pointAdded = QtCore.Signal(Point)
    segmentAdded = QtCore.Signal(Segment)

    def __init__(self, parent: MainWindow):
        super().__init__(parent)

        self.points: List[Point] = []
        self.segments: List[Segment] = []

        self.controller: Controller = Controller(self)

        self.setMouseTracking(True)

    def setController(self, controller: Controller) -> None:
        self.controller = controller

    def addPoint(self, point: Point) -> None:
        self.points.append(point)
        self.pointAdded.emit(point)

    def addSegment(self, segment: Segment) -> None:
        self.segments.append(segment)
        self.segmentAdded.emit(segment)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        point = event.localPos()
        self.mouseMoved.emit(point)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        point = event.localPos()
        self.mousePressed.emit(point)


class Controller(object):

    def __init__(self, sketch: Sketch):
        self.sketch = sketch


class CancelController(Controller):
    pass


class PointController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        self.sketch.addPoint(point)


class LineController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)
        self.sketch.mouseMoved.connect(self.onMouseMoved)

    def onMousePressed(self, point: Point) -> None:
        pass

    def onMouseMoved(self, point: Point) -> None:
        pass


class ParallelController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        pass


class PerpendicularController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        pass


class CoincidentController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        pass


class FixedController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        pass


class AngleController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        pass


class VerticalController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        pass


class HorizontalController(Controller):

    def __init__(self, sketch: Sketch):
        super().__init__(sketch)

        self.sketch.mousePressed.connect(self.onMousePressed)

    def onMousePressed(self, point: Point) -> None:
        pass

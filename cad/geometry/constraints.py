from PyQt5.QtWidgets import QInputDialog

from cad.drawing import Segment, Point


class SketchMode:
    sketch = None

    def __init__(self, sketch):
        self.sketch = sketch

    def mousePressedHandler(self):
        pass

    def mouseMovedHandler(self):
        pass


class DrawSegment(SketchMode):

    def mousePressedHandler(self):
        p1 = self.sketch.getPressedPosition()
        p2 = self.sketch.getCurrentPosition()

        segment = Segment(p1, p2)
        self.sketch.segments.append(segment)

    def mouseMovedHandler(self):
        if self.sketch.isMousePressed():
            position = self.sketch.getCurrentPosition()
            self.sketch.segments[-1].setP2(position)


class DrawPoint(SketchMode):

    def mousePressedHandler(self):
        position = self.sketch.getPressedPosition()

        point = Point(position)
        self.sketch.points.append(point)


class Constraint(SketchMode):
    pass


class Coincident(Constraint):

    def __init__(self, *args):
        super().__init__(*args)

        self.selected = None

    def mousePressedHandler(self):
        selected = self.sketch.getSelected()

        if isinstance(selected, Point):

            if self.selected is None:
                self.selected = selected

            elif isinstance(self.selected, Point):
                selected.setX(self.selected.x())
                selected.setY(self.selected.y())


class Parallel(Constraint):

    def __init__(self, *args):
        super().__init__(*args)

        self.selected = None

    def mousePressedHandler(self):
        selected = self.sketch.getSelected()

        if isinstance(selected, Segment):

            if self.selected is None:
                self.selected = selected

            elif isinstance(selected, Segment):
                selected.setAngle(self.selected.angle())
                self.selected = None


class Perpendicular(Constraint):

    def __init__(self, *args):
        super().__init__(*args)

        self.selected = None

    def mousePressedHandler(self):
        selected = self.sketch.getSelected()

        if isinstance(selected, Segment):

            if self.selected is None:
                self.selected = selected

            elif isinstance(self.selected, Segment):
                selected.setAngle(self.selected.angle() + 90)
                self.selected = None


class Angle(Constraint):

    def __init__(self, *args):
        super().__init__(*args)

        self.angle, ok = self.askAngleValue()

    def askAngleValue(self):
        label = 'Input angle value:'
        title = 'Set angle constraint'
        return QInputDialog.getDouble(self.sketch.parent(), title, label, 0)

    def mousePressedHandler(self):
        selected = self.sketch.getSelected()
        if isinstance(selected, Segment):
            selected.setAngle(self.angle)


class Horizontal(Constraint):

    def mousePressedHandler(self):
        selected = self.sketch.getSelected()
        if isinstance(selected, Segment):
            selected.setAngle(0)


class Vertical(Constraint):

    def mousePressedHandler(self):
        selected = self.sketch.getSelected()
        if isinstance(selected, Segment):
            selected.setAngle(90)


class Length(Constraint):

    def __init__(self, *args):
        super().__init__(*args)

        self.length, ok = self.askLengthValue()

    def askLengthValue(self):
        label = 'Input length value:'
        title = 'Set length constraint'
        return QInputDialog.getDouble(self.sketch.parent(), title, label, 0, 0)

    def mousePressedHandler(self):
        selected = self.sketch.getSelected()
        if isinstance(selected, Segment):
            selected.setLength(self.length)

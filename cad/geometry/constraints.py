from abc import abstractmethod

from .objects import Line, Point


class Constraint:

    @abstractmethod
    def apply(self, obj):
        pass


class Coincident(Constraint):

    def __init__(self):
        self.selected = None

    def apply(self, obj):
        if self.selected is None:
            self.selected = obj
        else:
            if isinstance(obj, Point):
                if isinstance(self.selected, Point):
                    obj.setX(self.selected.x())
                    obj.setY(self.selected.y())


class Parallel(Constraint):

    def __init__(self):
        self.selected = None

    def apply(self, obj):
        if isinstance(obj, Line):
            if self.selected is None:
                self.selected = obj
            else:
                angle = self.selected.angle()
                obj.setAngle(angle)
                self.selected = None


class Perpendicular(Constraint):

    def __init__(self):
        self.selected = None

    def apply(self, obj):
        if isinstance(obj, Line):
            if self.selected is None:
                self.selected = obj
            else:
                angle = self.selected.angle()
                obj.setAngle(angle + 90)
                self.selected = None


class Angle(Constraint):

    def __init__(self, value):
        self.value = None

        self.setValue(value)

    def setValue(self, value):
        self.value = value

    def apply(self, obj):
        if isinstance(obj, Line):
            obj.setAngle(self.value)


class Horizontal(Constraint):

    def apply(self, obj):
        if isinstance(obj, Line):
            obj.setAngle(0)


class Vertical(Constraint):

    def apply(self, obj):
        if isinstance(obj, Line):
            obj.setAngle(90)


class Length(Constraint):

    def __init__(self, value):
        self.value = None

        self.setValue(value)

    def setValue(self, value):
        if value < 0:
            message = 'Given value is invalid. Expected positive value'
            raise Exception(message)
        self.value = value

    def apply(self, obj):
        if isinstance(obj, Line):
            obj.setLength(self.value)

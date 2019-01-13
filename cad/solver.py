from abc import abstractmethod

import numpy as np
from scipy.optimize import fsolve

from cad.figures import Point, Line


class System(object):

    def __init__(self, sketch):
        self.sketch = sketch
        self.constraints = []

    @property
    def points(self) -> list:
        points = []
        for line in self.sketch.lines:
            points.extend(line.points)
        for point in self.sketch.points:
            points.append(point)
        return points

    def addConstraint(self, constraint):
        self.constraints.append(constraint)

    def recount(self):
        if len(self.x0):
            y = self.solve()
            for i, point in enumerate(self.points):
                for j, prop in enumerate(('x', 'y')):
                    n = i * 2 + j
                    setattr(point, prop, y[n])

    def solve(self):
        result = fsolve(self.system, self.x0, full_output=False, xtol=1e-2)
        return [round(y, 1) for y in result]

    def system(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros(shape=x.shape, dtype=x.dtype)

        for i, point in enumerate(self.points):
            for j, coordinate in enumerate(point.coordinates):
                n = i * 2 + j
                y[n] = 2 * (x[n] - coordinate)

        for i, constraint in enumerate(self.constraints):
            n = len(self.points) * 2 + i
            constraint.apply(self, x, y, n)

        return y

    @property
    def x0(self) -> np.ndarray:
        size = len(self.points) * 2 + len(self.constraints)
        y = np.zeros(shape=(size, ), dtype=float)
        return y


class Handler:

    def mouseMoved(self, sketch):
        pass

    def mousePressed(self, sketch):
        pass

    def mouseReleased(self, sketch):
        pass


class DisableHandler(Handler):
    pass


class LineDrawing(Handler):

    def mousePressed(self, sketch):
        p1 = sketch.getPressedPosition()
        p2 = sketch.getCurrentPosition()

        sketch.addLine(Line(p1, p2))
        sketch.update()

    def mouseMoved(self, sketch):
        if sketch.isMousePressed():
            sketch.lines[-1].p2 = sketch.getCurrentPosition()
            sketch.update()


class PointDrawing(Handler):

    def mousePressed(self, sketch):
        point = sketch.getPressedPosition()
        sketch.addPoint(point)
        sketch.update()


class Constraint(object):

    @abstractmethod
    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        pass


class Length(Constraint):

    def __init__(self, line: Line, length: float):
        self.line = line
        self.length = length

    @property
    def p1(self) -> Point:
        return self.line.p1

    @property
    def p2(self) -> Point:
        return self.line.p2

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i1 = system.points.index(self.p1) * 2
        i2 = system.points.index(self.p2) * 2

        dx = x[i2] - x[i1]
        dy = x[i2 + 1] - x[i1 + 1]

        y[i2] += 2 * x[n] * dx
        y[i1] -= 2 * x[n] * dx

        y[i2 + 1] += 2 * x[n] * dy
        y[i1 + 1] -= 2 * x[n] * dy

        y[n] = dx ** 2 + dy ** 2 - self.length ** 2


class LengthHandler(Handler):

    def __init__(self, length: float):
        self.length = length

    def mousePressed(self, sketch):
        line = sketch.getActiveLine()
        if line:
            constraint = Length(line, self.length)
            sketch.system.addConstraint(constraint)
            sketch.update()


class AngleHandler(Handler):

    def __init__(self, angle: float):
        self.angle = angle

    def mousePressed(self, sketch):
        line = sketch.getActiveLine()
        if line:
            constraint = Angle(line, self.angle)
            sketch.system.addConstraint(constraint)
            sketch.update()


class FixingX(Constraint):

    def __init__(self, point: Point, value: float):
        self.point = point
        self.value = value

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i = system.points.index(self.point) * 2

        y[i] += x[n]

        y[n] = x[i] - self.value


class FixingY(Constraint):

    def __init__(self, point: Point, value: float):
        self.point = point
        self.value = value

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i = system.points.index(self.point) * 2 + 1

        y[i] += x[n]

        y[n] = x[i] - self.value


class Angle(Constraint):

    def __init__(self, line: Line, angle: float):
        self.line = line
        self.tan = np.tan(angle * np.pi / 180)

    @property
    def p1(self) -> Point:
        return self.line.p1

    @property
    def p2(self) -> Point:
        return self.line.p2

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i1 = system.points.index(self.p1) * 2
        i2 = system.points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[i2 + 1] += x[n] * self.tan
        y[i1 + 1] -= x[n] * self.tan

        y[n] = x[i2 + 1] - x[i1 + 1] - (x[i2] - x[i1]) * self.tan


class VerticalHandler(Handler):

    def mousePressed(self, sketch):
        line = sketch.getActiveLine()
        if line:
            sketch.system.addConstraint(Vertical(line))
            sketch.update()


class HorizontalHandler(Handler):

    def mousePressed(self, sketch):
        line = sketch.getActiveLine()
        if line:
            constraint = Horizontal(line)
            sketch.system.addConstraint(constraint)
            sketch.update()


class Vertical(Constraint, Handler):

    def __init__(self, line: Line):
        self.line = line

    @property
    def p1(self) -> Point:
        return self.line.p1

    @property
    def p2(self) -> Point:
        return self.line.p2

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i1 = system.points.index(self.p1) * 2
        i2 = system.points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class Horizontal(Constraint):

    def __init__(self, line: Line):
        self.line = line

    @property
    def p1(self) -> Point:
        return self.line.p1

    @property
    def p2(self) -> Point:
        return self.line.p2

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i1 = system.points.index(self.p1) * 2 + 1
        i2 = system.points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class CoincidentHandler(Handler):

    def __init__(self):
        self.p1 = None

    def mousePressed(self, sketch):
        point = sketch.getActivePoint()
        if point:
            if not self.p1:
                self.p1 = point
                return True
            else:
                sketch.system.addConstraint(CoincidentX(self.p1, point))
                sketch.system.addConstraint(CoincidentX(self.p1, point))

                self.p1 = None


class CoincidentX(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i1 = system.points.index(self.p1) * 2
        i2 = system.points.index(self.p2) * 2

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]


class CoincidentY(Constraint):

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def apply(self, system: System, x: np.ndarray, y: np.ndarray, n: int):
        i1 = system.points.index(self.p1) * 2 + 1
        i2 = system.points.index(self.p2) * 2 + 1

        y[i2] += x[n]
        y[i1] -= x[n]

        y[n] = x[i2] - x[i1]

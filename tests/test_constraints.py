import unittest

import numpy as np

from time import time

from cad.core import Point, Segment, p2p, angle
from cad.solver import Solver, SolutionNotFound
from cad.constraints import Length, Vertical, FixingX, FixingY, \
    CoincidentX, CoincidentY, Parallel, Angle, Perpendicular, Horizontal


class ConstraintTestCase(unittest.TestCase):

    def assertClose(self, expected: float, actual: float):
        self.assertTrue(np.isclose(expected, actual, 1e-1))

    def setUp(self) -> None:
        self.solver = Solver()

    def assertLength(self, p1: Point, p2: Point, length: float):
        actual = p2p(p1, p2)
        self.assertClose(length, actual)

    def assertCoincidentX(self, p1: Point, p2: Point):
        self.assertClose(p1.x(), p2.x())

    def assertCoincidentY(self, p1: Point, p2: Point):
        self.assertClose(p1.y(), p2.y())

    def assertCoincident(self, p1: Point, p2: Point):
        self.assertCoincidentX(p1, p2)
        self.assertCoincidentY(p1, p2)

    def assertFixingX(self, point: Point, lock: Point):
        self.assertClose(point.x(), lock.x())

    def assertFixingY(self, point: Point, lock: Point):
        self.assertClose(point.y(), lock.y())

    def assertFixing(self, point: Point, lock: Point):
        self.assertFixingX(point, lock)
        self.assertFixingY(point, lock)

    def assertVertical(self, p1: Point, p2: Point):
        self.assertClose(p1.x(), p2.x())

    def assertHorizontal(self, p1: Point, p2: Point):
        self.assertClose(p1.y(), p2.y())

    def assertParallel(self, p1: Point, p2: Point, p3: Point, p4: Point):
        l1 = Segment(p1, p2)
        l2 = Segment(p3, p4)
        value = np.round(angle(l1, l2))
        self.assertIn(value, [0, 180, 360])

    def assertAngle(self, l1: Segment, l2: Segment, value: float):
        actual = angle(l1, l2)
        self.assertClose(actual, value)

    def assertPerpendicular(self, p1: Point, p2: Point, p3: Point, p4: Point):
        l1 = Segment(p1, p2)
        l2 = Segment(p3, p4)
        value = np.round(angle(l1, l2))
        self.assertIn(value, [90, 270])


class LengthConstraintTestCase(ConstraintTestCase):

    def test_length(self):
        p1 = Point(10, 15)
        p2 = Point(20, 30)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraint = Length(p1, p2, 20)
        self.solver.addConstraint(constraint)

        p1, p2 = self.solver.recount()
        self.assertLength(p1, p2, constraint.length)


class CoincidentConstraintTestCase(ConstraintTestCase):

    def test_coincident(self):
        p1 = Point(15, 30)
        p2 = Point(20, 25)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraintX = CoincidentX(p1, p2)
        constraintY = CoincidentY(p1, p2)

        self.solver.addConstraint(constraintX)
        self.solver.addConstraint(constraintY)

        p1, p2 = self.solver.recount()
        self.assertCoincident(p1, p2)


class FixingConstraintTestCase(ConstraintTestCase):

    def test_fixing(self):
        point = Point(10, 20)
        self.solver.addPoint(point)

        x, y = 15, 15
        constraintX = FixingX(point, x)
        constraintY = FixingY(point, y)

        self.solver.addConstraint(constraintX)
        self.solver.addConstraint(constraintY)

        point,  = self.solver.recount()
        self.assertFixing(point, Point(x, y))


class VerticalConstraintTestCase(ConstraintTestCase):

    def test_vertical(self):
        p1 = Point(10, 15)
        p2 = Point(20, 25)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraint = Vertical(p1, p2)
        self.solver.addConstraint(constraint)

        p1, p2 = self.solver.recount()
        self.assertVertical(p1, p2)


class HorizontalConstraintTestCase(ConstraintTestCase):

    def test_horizontal(self):
        p1 = Point(10, 15)
        p2 = Point(20, 25)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraint = Horizontal(p1, p2)
        self.solver.addConstraint(constraint)

        p1, p2 = self.solver.recount()
        self.assertHorizontal(p1, p2)


class ParallelConstraintTestCase(ConstraintTestCase):

    def test_parallel(self):
        p1 = Point(10, 10)
        p2 = Point(30, 30)
        p3 = Point(13, 28)
        p4 = Point(25, 27)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)
        self.solver.addPoint(p3)
        self.solver.addPoint(p4)

        constraint = Parallel(p1, p2, p3, p4)
        self.solver.addConstraint(constraint)

        p1, p2, p3, p4 = self.solver.recount()
        self.assertParallel(p1, p2, p3, p4)


class PerpendicularConstraintTestCase(ConstraintTestCase):

    def test_perpendicular(self):
        p1 = Point(10, 10)
        p2 = Point(30, 30)
        p3 = Point(12, 28)
        p4 = Point(25, 27)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)
        self.solver.addPoint(p3)
        self.solver.addPoint(p4)

        constraint = Perpendicular(p1, p2, p3, p4)
        self.solver.addConstraint(constraint)

        p1, p2, p3, p4 = self.solver.recount()
        self.assertPerpendicular(p1, p2, p3, p4)


class AngleConstraintTestCase(ConstraintTestCase):

    def test_perpendicular(self):
        p1 = Point(10, 10)
        p2 = Point(10, 30)
        p3 = Point(15, 15)
        p4 = Point(30, 30)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)
        self.solver.addPoint(p3)
        self.solver.addPoint(p4)

        constraint = Angle(p1, p2, p3, p4, 60)
        self.solver.addConstraint(constraint)

        p1, p2, p3, p4 = self.solver.recount()
        l1 = Segment(p1, p2)
        l2 = Segment(p3, p4)
        self.assertAngle(l1, l2, constraint.degrees)


class ComplexConstraintsTestCase(ConstraintTestCase):

    def test_constraints(self):
        points = [
            Point(i, i) for i in range(9)
        ]

        constraints = [
            FixingY(points[0], 0),
            FixingX(points[0], 0),
            Vertical(points[0], points[1]),
            Length(points[0], points[1], 10),
            CoincidentX(points[1], points[1]),
            CoincidentY(points[2], points[2]),
            Horizontal(points[2], points[3]),
            Length(points[2], points[3], 10),
            FixingY(points[3], 10),
            FixingX(points[3], 10),
            CoincidentY(points[3], points[4]),
            CoincidentX(points[3], points[4]),
            Perpendicular(points[2], points[3], points[4], points[5]),
            CoincidentX(points[5], points[6]),
            CoincidentY(points[5], points[6]),
            Horizontal(points[6], points[7]),
            Length(points[6], points[7], 10),
            Parallel(points[7], points[8], points[5], points[4]),
            Horizontal(points[8], points[0]),
        ]

        self.solver.points.extend(points)
        self.solver.constraints.extend(constraints)

        start = time()
        points = self.solver.recount()
        calc_time = time() - start

        self.assertFixing(points[0], Point(0, 0))
        self.assertLength(points[0], points[1], 10)
        self.assertVertical(points[0], points[1])
        self.assertCoincident(points[1], points[2])
        self.assertHorizontal(points[2], points[3])
        self.assertLength(points[2], points[3], 10)
        self.assertFixing(points[3], Point(10, 10))
        self.assertPerpendicular(points[2], points[3], points[4], points[5])
        self.assertCoincident(points[5], points[6])
        self.assertHorizontal(points[6], points[7])
        self.assertLength(points[6], points[7], 10)
        self.assertHorizontal(points[8], points[0])
        self.assertLength(points[8], points[0], 20)

        self.assertLess(calc_time, 0.1)


class SolutionNotFoundTestCase(ConstraintTestCase):

    def test_not_solution(self):
        p1 = Point(10, 10)
        p2 = Point(20, 20)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        self.solver.addConstraint(Length(p1, p2, 20))
        self.solver.addConstraint(Length(p1, p2, 10))

        with self.assertRaises(SolutionNotFound):
            self.solver.recount()

        try:
            self.solver.recount()
        except SolutionNotFound as e:
            msg = str(e)
            self.assertIsInstance(msg, str)


if __name__ == '__main__':
    unittest.main()

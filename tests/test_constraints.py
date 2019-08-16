import unittest

import numpy as np

from time import time

from cad.core import Point, Segment, p2p, angle
from cad.solver import Solver, SolutionNotFound
from cad import constraints


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

    def assertFixedX(self, point: Point, lock: Point):
        self.assertClose(point.x(), lock.x())

    def assertFixedY(self, point: Point, lock: Point):
        self.assertClose(point.y(), lock.y())

    def assertFixed(self, point: Point, lock: Point):
        self.assertFixedX(point, lock)
        self.assertFixedY(point, lock)

    def assertVertical(self, p1: Point, p2: Point):
        self.assertClose(p1.x(), p2.x())

    def assertHorizontal(self, p1: Point, p2: Point):
        self.assertClose(p1.y(), p2.y())

    def assertParallel(self, p1: Point, p2: Point, p3: Point, p4: Point):
        l1 = Segment(p1, p2)
        l2 = Segment(p3, p4)
        value = np.round(angle(l1, l2), -1)
        self.assertIn(value, [0, 180, 360])

    def assertAngle(self, l1: Segment, l2: Segment, value: float):
        actual = angle(l1, l2)
        self.assertClose(actual, value)

    def assertPerpendicular(self, p1: Point, p2: Point, p3: Point, p4: Point):
        l1 = Segment(p1, p2)
        l2 = Segment(p3, p4)
        value = np.round(angle(l1, l2), -1)
        self.assertIn(value, [90, 270])


class LengthConstraintTestCase(ConstraintTestCase):

    def test_length_constraint(self):
        p1 = Point(10, 15)
        p2 = Point(20, 30)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraint = constraints.LengthConstraint(0, 2, 20)
        self.solver.addConstraint(constraint)

        p1, p2 = self.solver.recount()
        self.assertLength(p1, p2, constraint.length)


class CoincidentConstraintTestCase(ConstraintTestCase):

    def test_coincident_constraint(self):
        p1 = Point(15, 30)
        p2 = Point(20, 25)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraintX = constraints.CoincidentConstraint(0, 2)
        constraintY = constraints.CoincidentConstraint(1, 3)

        self.solver.addConstraint(constraintX)
        self.solver.addConstraint(constraintY)

        p1, p2 = self.solver.recount()
        self.assertCoincident(p1, p2)


class FixedConstraintTestCase(ConstraintTestCase):

    def test_fixed_constraint(self):
        point = Point(10, 20)
        self.solver.addPoint(point)

        x, y = 15, 15
        constraintX = constraints.FixedConstraint(0, x)
        constraintY = constraints.FixedConstraint(1, y)

        self.solver.addConstraint(constraintX)
        self.solver.addConstraint(constraintY)

        point,  = self.solver.recount()
        self.assertFixed(point, Point(x, y))


class VerticalConstraintTestCase(ConstraintTestCase):

    def test_vertical_constraint(self):
        p1 = Point(10, 15)
        p2 = Point(20, 25)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraint = constraints.VerticalConstraint(0, 2)
        self.solver.addConstraint(constraint)

        p1, p2 = self.solver.recount()
        self.assertVertical(p1, p2)


class HorizontalConstraintTestCase(ConstraintTestCase):

    def test_horizontal_constraint(self):
        p1 = Point(10, 15)
        p2 = Point(20, 25)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        constraint = constraints.HorizontalConstraint(1, 3)
        self.solver.addConstraint(constraint)

        p1, p2 = self.solver.recount()
        self.assertHorizontal(p1, p2)


class ParallelConstraintTestCase(ConstraintTestCase):

    def test_parallel_constraint(self):
        p1 = Point(10, 10)
        p2 = Point(30, 30)
        p3 = Point(13, 28)
        p4 = Point(25, 27)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)
        self.solver.addPoint(p3)
        self.solver.addPoint(p4)

        constraint = constraints.ParallelConstraint(0, 2, 4, 6)
        self.solver.addConstraint(constraint)

        p1, p2, p3, p4 = self.solver.recount()
        self.assertParallel(p1, p2, p3, p4)


class PerpendicularConstraintTestCase(ConstraintTestCase):

    def test_perpendicular_constraint(self):
        p1 = Point(10, 10)
        p2 = Point(30, 30)
        p3 = Point(12, 28)
        p4 = Point(25, 27)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)
        self.solver.addPoint(p3)
        self.solver.addPoint(p4)

        constraint = constraints.PerpendicularConstraint(0, 2, 4, 6)
        self.solver.addConstraint(constraint)

        p1, p2, p3, p4 = self.solver.recount()
        self.assertPerpendicular(p1, p2, p3, p4)


class AngleConstraintTestCase(ConstraintTestCase):

    def test_perpendicular_constraint(self):
        p1 = Point(10, 10)
        p2 = Point(10, 30)
        p3 = Point(15, 15)
        p4 = Point(30, 30)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)
        self.solver.addPoint(p3)
        self.solver.addPoint(p4)

        constraint = constraints.AngleConstraint(0, 2, 4, 6, 60)
        self.solver.addConstraint(constraint)

        p1, p2, p3, p4 = self.solver.recount()
        l1 = Segment(p1, p2)
        l2 = Segment(p3, p4)
        self.assertAngle(l1, l2, 60)


class ComplexConstraintsTestCase(ConstraintTestCase):

    def test_constraints(self):
        points = [
            Point(i, i) for i in range(12)
        ]

        constraints_list = [
            constraints.FixedConstraint(0, 10),           # p0.x = 10
            constraints.FixedConstraint(1, 10),           # p0.y = 10

            constraints.VerticalConstraint(0, 2),         # p0.x = p1.x
            constraints.LengthConstraint(0, 2, 10),       # dist(p0, p1) = 10

            constraints.CoincidentConstraint(2, 4),       # p1.x = p2.x
            constraints.CoincidentConstraint(3, 5),       # p1.y = p2.y

            constraints.HorizontalConstraint(5, 7),       # p2.y = p3.y
            constraints.LengthConstraint(4, 6, 10),       # dist(p2, p3) = 10

            constraints.CoincidentConstraint(6, 8),       # p3.x = p4.x
            constraints.CoincidentConstraint(7, 9),       # p3.y = p4.y

            constraints.ParallelConstraint(8, 10, 0, 2),  # p4, p5 _|_ p0, p1
            constraints.LengthConstraint(8, 10, 10),      # dist(p4, p5) = 10

            constraints.CoincidentConstraint(10, 12),     # p5.x = p6.x
            constraints.CoincidentConstraint(11, 13),     # p5.y = p6.y

            constraints.PerpendicularConstraint(12, 14, 0, 2),
            constraints.LengthConstraint(12, 14, 10),     # dist(p6, p7) = 10

            constraints.CoincidentConstraint(14, 16),     # p7.x = p8.x
            constraints.CoincidentConstraint(15, 17),     # p7.y = p8.y

            constraints.PerpendicularConstraint(16, 18, 4, 6),
            constraints.LengthConstraint(16, 18, 20),     # dist(p8, p9) = 20

            constraints.CoincidentConstraint(18, 20),     # p9.x = p10.x
            constraints.CoincidentConstraint(19, 21),     # p9.y = p10.y

            constraints.CoincidentConstraint(22, 0),      # p11.x = p0.x
            constraints.CoincidentConstraint(23, 1),      # p11.y = p0.y
        ]

        self.solver.points.extend(points)
        self.solver.constraints.extend(constraints_list)

        start = time()
        points = self.solver.recount()
        stop = time()

        self.assertFixed(points[0], Point(10, 10))
        self.assertVertical(points[0], points[1])
        self.assertLength(points[0], points[1], 10)
        self.assertCoincident(points[1], points[2])
        self.assertHorizontal(points[2], points[3])
        self.assertLength(points[2], points[3], 10)
        self.assertCoincident(points[3], points[4])
        self.assertParallel(points[0], points[1], points[4], points[5])
        self.assertLength(points[4], points[5], 10)
        self.assertCoincident(points[5], points[6])
        self.assertPerpendicular(points[0], points[1], points[6], points[7])
        self.assertLength(points[6], points[7], 10)
        self.assertCoincident(points[7], points[8])
        self.assertPerpendicular(points[2], points[3], points[8], points[9])
        self.assertLength(points[8], points[9], 20)
        self.assertCoincident(points[9], points[10])
        self.assertHorizontal(points[10], points[11])
        self.assertCoincident(points[11], points[0])

        calculate_time = stop - start
        self.assertLess(calculate_time, 0.1)


class SolutionNotFoundTestCase(ConstraintTestCase):

    def test_not_solution(self):
        p1 = Point(10, 10)
        p2 = Point(20, 20)

        self.solver.addPoint(p1)
        self.solver.addPoint(p2)

        self.solver.addConstraint(constraints.LengthConstraint(0, 2, 20))
        self.solver.addConstraint(constraints.LengthConstraint(0, 2, 10))

        with self.assertRaises(SolutionNotFound):
            self.solver.recount()

        try:
            self.solver.recount()
        except SolutionNotFound as e:
            msg = str(e)
            self.assertIsInstance(msg, str)


if __name__ == '__main__':
    unittest.main()

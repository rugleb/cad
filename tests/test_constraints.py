import unittest

from cad.algebra import Point, Solver, p2p
from cad.algebra import CoincidentY, CoincidentX, Length
from cad.algebra import FixingX, FixingY, Vertical, Horizontal


class ConstraintTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.solver = Solver()

    def assertLength(self, p1: Point, p2: Point, length: float):
        actual = p2p(p1, p2)
        self.assertEqual(length, actual)

    def assertCoincidentX(self, p1: Point, p2: Point):
        self.assertEqual(p1.x(), p2.x())

    def assertCoincidentY(self, p1: Point, p2: Point):
        self.assertEqual(p1.y(), p2.y())

    def assertCoincident(self, p1: Point, p2: Point):
        self.assertCoincidentX(p1, p2)
        self.assertCoincidentY(p1, p2)

    def assertFixingX(self, point: Point, lock: Point):
        self.assertEqual(point.x(), lock.x())

    def assertFixingY(self, point: Point, lock: Point):
        self.assertEqual(point.y(), lock.y())

    def assertFixing(self, point: Point, lock: Point):
        self.assertFixingX(point, lock)
        self.assertFixingY(point, lock)

    def assertVertical(self, p1: Point, p2: Point):
        self.assertEqual(p1.x(), p2.x())

    def assertHorizontal(self, p1: Point, p2: Point):
        self.assertEqual(p1.y(), p2.y())


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


if __name__ == '__main__':
    unittest.main()

import unittest

from cad.algebra import Point, Solver, p2p
from cad.algebra import CoincidentY, CoincidentX, Length


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


if __name__ == '__main__':
    unittest.main()

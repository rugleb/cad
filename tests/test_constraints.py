import unittest

from cad.algebra import Length, Point, Solver, p2p


class ConstraintTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.solver = Solver()

    def assertLength(self, p1: Point, p2: Point, length: float):
        actual = p2p(p1, p2)
        self.assertEqual(length, actual)


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


if __name__ == '__main__':
    unittest.main()

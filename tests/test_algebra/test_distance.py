import unittest

from cad.algebra.distance import Point, Line, p2p, p2l, sqrt


class DistanceTestCase(unittest.TestCase):

    def test_point_2_point_method(self):
        cases = [
            (Point(0, 0), Point(5, 0), 5),
            (Point(0, 0), Point(0, 5), 5),
            (Point(0, 0), Point(5, 5), sqrt(50, 2)),
            (Point(5, 5), Point(0, 0), sqrt(50, 2)),
        ]

        for p1, p2, expected in cases:
            actual = p2p(p1, p2)
            self.assertEqual(expected, actual)

    def test_point_2_line_method(self):
        cases = [
            (Line(0, 0, 5, 5), Point(0, 0), 0),
            (Line(0, 0, 5, 5), Point(5, 5), 0),
            (Line(4, 4, 4, 0), Point(0, 4), 4),
            (Line(1, 1, 2, 2), Point(0, 0), 0),
            (Line(4, 4, 4, 4), Point(5, 5), sqrt(2)),
        ]

        for line, point, expected in cases:
            actual = p2l(point, line)
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

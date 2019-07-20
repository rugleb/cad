import unittest

from cad.algebra import Point, Line, p2p, p2l, p2s, sqrt


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

    def test_point_2_segment_method(self):
        cases = [
            (Line(1, 1, 3, 3), Point(1, 1), 0),
            (Line(1, 1, 3, 3), Point(2, 2), 0),
            (Line(1, 1, 3, 3), Point(3, 3), 0),
            (Line(1, 1, 3, 3), Point(0, 0), sqrt(2)),
            (Line(1, 1, 3, 3), Point(4, 4), sqrt(2)),
            (Line(0, 0, 0, 2), Point(4, 3), 4),
            (Line(0, 0, 4, 0), Point(3, 4), 4),
            (Line(3, 3, 1, 1), Point(1, 1), 0),
            (Line(3, 3, 1, 1), Point(2, 2), 0),
            (Line(3, 3, 1, 1), Point(3, 3), 0),
            (Line(3, 3, 1, 1), Point(0, 0), sqrt(2)),
            (Line(3, 3, 1, 1), Point(4, 4), sqrt(2)),
            (Line(0, 4, 0, 0), Point(4, 3), 4),
            (Line(4, 0, 0, 0), Point(3, 4), 4),
            (Line(0, 3, 3, 0), Point(0, 0), sqrt(18) / 2),
            (Line(3, 0, 0, 3), Point(0, 0), sqrt(18) / 2),
        ]

        for line, point, expected in cases:
            actual = p2s(point, line)
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

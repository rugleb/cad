import unittest

import numpy as np

from cad.algebra import Point, Segment, p2p, p2l, p2s, sqrt


class DistanceTestCase(unittest.TestCase):

    def test_point_2_point_method(self):
        cases = [
            (Point(0, 0), Point(5, 0), 5),
            (Point(0, 0), Point(0, 5), 5),
            (Point(0, 0), Point(5, 5), sqrt(50)),
            (Point(5, 5), Point(0, 0), sqrt(50)),
        ]

        for p1, p2, expected in cases:
            actual = p2p(p1, p2)
            self.assertTrue(np.isclose(expected, actual))

    def test_point_2_line_method(self):
        cases = [
            (Segment(0, 0, 5, 5), Point(0, 0), 0),
            (Segment(0, 0, 5, 5), Point(5, 5), 0),
            (Segment(4, 4, 4, 0), Point(0, 4), 4),
            (Segment(1, 1, 2, 2), Point(0, 0), 0),
            (Segment(4, 4, 4, 4), Point(5, 5), sqrt(2)),
        ]

        for line, point, expected in cases:
            actual = p2l(point, line)
            self.assertTrue(np.isclose(expected, actual))

    def test_point_2_segment_method(self):
        cases = [
            (Segment(1, 1, 3, 3), Point(1, 1), 0),
            (Segment(1, 1, 3, 3), Point(2, 2), 0),
            (Segment(1, 1, 3, 3), Point(3, 3), 0),
            (Segment(1, 1, 3, 3), Point(0, 0), sqrt(2)),
            (Segment(1, 1, 3, 3), Point(4, 4), sqrt(2)),
            (Segment(0, 0, 4, 0), Point(3, 4), 4),
            (Segment(3, 3, 1, 1), Point(1, 1), 0),
            (Segment(3, 3, 1, 1), Point(2, 2), 0),
            (Segment(3, 3, 1, 1), Point(3, 3), 0),
            (Segment(3, 3, 1, 1), Point(0, 0), sqrt(2)),
            (Segment(3, 3, 1, 1), Point(4, 4), sqrt(2)),
            (Segment(0, 4, 0, 0), Point(4, 3), 4),
            (Segment(4, 0, 0, 0), Point(3, 4), 4),
            (Segment(0, 3, 3, 0), Point(0, 0), sqrt(18) / 2),
            (Segment(3, 0, 0, 3), Point(0, 0), sqrt(18) / 2),
        ]

        for line, point, expected in cases:
            actual = p2s(point, line)
            self.assertTrue(np.isclose(expected, actual))


if __name__ == '__main__':
    unittest.main()

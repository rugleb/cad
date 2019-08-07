import unittest

import numpy as np

from cad.algebra import Point, Segment, p2p, p2l, p2s


class DistanceTestCase(unittest.TestCase):

    def assertClose(self, expected: float, actual: float):
        expr = np.isclose(expected, actual)
        self.assertTrue(expr)

    def test_p2p_method(self):
        cases = [
            (Point(0, 0), Point(5, 0), 5),
            (Point(0, 0), Point(0, 5), 5),
            (Point(0, 0), Point(5, 5), np.sqrt(50)),
            (Point(5, 5), Point(0, 0), np.sqrt(50)),
        ]

        for p1, p2, expected in cases:
            actual = p2p(p1, p2)
            self.assertClose(expected, actual)

    def test_p2l_method(self):
        cases = [
            # diagonal segment
            (Point(0, 0), Segment(1, 1, 2, 2), 0),
            (Point(1, 1), Segment(1, 1, 2, 2), 0),
            (Point(2, 2), Segment(1, 1, 2, 2), 0),
            (Point(3, 3), Segment(1, 1, 2, 2), 0),
            (Point(1, 0), Segment(1, 1, 2, 2), np.sqrt(2) / 2),
            (Point(2, 3), Segment(1, 1, 2, 2), np.sqrt(2) / 2),

            # vertical segment
            (Point(1, 0), Segment(1, 1, 1, 2), 0),
            (Point(1, 1), Segment(1, 1, 1, 2), 0),
            (Point(1, 2), Segment(1, 1, 1, 2), 0),
            (Point(1, 3), Segment(1, 1, 1, 2), 0),
            (Point(0, 0), Segment(1, 1, 1, 2), 1),
            (Point(2, 2), Segment(1, 1, 1, 2), 1),

            # horizontal segment
            (Point(0, 1), Segment(1, 1, 2, 1), 0),
            (Point(1, 1), Segment(1, 1, 2, 1), 0),
            (Point(2, 1), Segment(1, 1, 2, 1), 0),
            (Point(3, 1), Segment(1, 1, 2, 1), 0),
            (Point(0, 0), Segment(1, 1, 2, 1), 1),
            (Point(2, 2), Segment(1, 1, 2, 1), 1),
        ]

        for point, segment, expected in cases:
            actual = p2l(point, segment)
            self.assertClose(expected, actual)

    def test_point_2_segment_method(self):
        cases = [
            # diagonal segment
            (Point(0, 0), Segment(1, 1, 2, 2), np.sqrt(2)),
            (Point(1, 1), Segment(1, 1, 2, 2), 0),
            (Point(2, 2), Segment(1, 1, 2, 2), 0),
            (Point(3, 3), Segment(1, 1, 2, 2), np.sqrt(2)),
            (Point(1, 0), Segment(1, 1, 2, 2), 1),
            (Point(2, 3), Segment(1, 1, 2, 2), 1),

            # vertical segment
            (Point(1, 0), Segment(1, 1, 1, 2), 1),
            (Point(1, 1), Segment(1, 1, 1, 2), 0),
            (Point(1, 2), Segment(1, 1, 1, 2), 0),
            (Point(1, 3), Segment(1, 1, 1, 2), 1),
            (Point(0, 0), Segment(1, 1, 1, 2), np.sqrt(2)),
            (Point(2, 3), Segment(1, 1, 1, 2), np.sqrt(2)),
            (Point(0, 2), Segment(1, 1, 1, 2), 1),
            (Point(2, 2), Segment(1, 1, 1, 2), 1),

            # # horizontal segment
            (Point(0, 1), Segment(1, 1, 2, 1), 1),
            (Point(1, 1), Segment(1, 1, 2, 1), 0),
            (Point(2, 1), Segment(1, 1, 2, 1), 0),
            (Point(3, 1), Segment(1, 1, 2, 1), 1),
            (Point(0, 0), Segment(1, 1, 2, 1), np.sqrt(2)),
            (Point(3, 2), Segment(1, 1, 2, 1), np.sqrt(2)),
            (Point(1, 2), Segment(1, 1, 2, 1), 1),
            (Point(1, 0), Segment(1, 1, 2, 1), 1),
        ]

        for point, segment, expected in cases:
            actual = p2s(point, segment)
            self.assertClose(expected, actual)


if __name__ == '__main__':
    unittest.main()

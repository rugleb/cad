import unittest

import numpy as np

from cad.algebra import Point, Segment, p2p, p2l, p2s, angle


class AlgebraTestCase(unittest.TestCase):

    def assertClose(self, expected: float, actual: float):
        message = f'Values are not close: {expected} !~ {actual}.'
        expr = np.isclose(expected, actual)
        self.assertTrue(expr, message)

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
            (Point(0, 0), Segment(1, 1, 1, 1), np.sqrt(2)),
            (Point(2, 2), Segment(1, 1, 1, 1), np.sqrt(2)),

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

    def test_p2s_method(self):
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

    def test_angle_method(self):
        cases = [
            (Segment(0, 0, 5, 0), Segment(0, 0, 5, 0), 0),
            (Segment(0, 0, 5, 5), Segment(0, 0, 5, 0), 45),
            (Segment(0, 0, 0, 5), Segment(0, 0, 5, 0), 90),
            (Segment(5, 0, 0, 0), Segment(0, 0, 5, 0), 180),
            (Segment(5, 5, 0, 0), Segment(0, 0, 5, 0), 225),
            (Segment(5, 5, 0, 0), Segment(0, 0, 0, 5), 135),
        ]

        for s1, s2, expected in cases:
            actual = angle(s1, s2)
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

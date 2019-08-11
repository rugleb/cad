import unittest

import numpy as np

from cad import core


class SegmentTestCase(unittest.TestCase):

    def test_is_vertical(self):
        segment = core.Segment(10, 10, 10, 20)
        self.assertTrue(segment.isVertical())

    def test_is_not_vertical(self):
        segment = core.Segment(10, 10, 20, 20)
        self.assertFalse(segment.isVertical())

    def test_is_horizontal(self):
        segment = core.Segment(10, 10, 20, 10)
        self.assertTrue(segment.isHorizontal())

    def test_is_not_horizontal(self):
        segment = core.Segment(10, 10, 20, 20)
        self.assertFalse(segment.isHorizontal())

    def test_points_method(self):
        p1 = core.Point(10, 10)
        p2 = core.Point(20, 20)
        segment = core.Segment(p1, p2)

        expected = p1, p2
        actual = segment.points()
        self.assertEqual(expected, actual)

    def test_coordinates_method(self):
        x1, y1, x2, y2 = 0, 5, 10, 20
        segment = core.Segment(x1, y1, x2, y2)

        expected = x1, y1, x2, y2
        actual = segment.coordinates()
        self.assertEqual(expected, actual)


class DrawStyleTestCase(unittest.TestCase):

    def test_on_types(self):
        for style in core.DrawStyle:
            self.assertIsInstance(style.width(), float)
            self.assertIsInstance(style.color(), core.Color)


class AlgebraTestCase(unittest.TestCase):

    def assertClose(self, expected: float, actual: float):
        message = f'Values are not close: {expected} !~ {actual}.'
        expr = np.isclose(expected, actual)
        self.assertTrue(expr, message)

    def test_p2p_method(self):
        cases = [
            (core.Point(0, 0), core.Point(5, 0), 5),
            (core.Point(0, 0), core.Point(0, 5), 5),
            (core.Point(0, 0), core.Point(5, 5), np.sqrt(50)),
            (core.Point(5, 5), core.Point(0, 0), np.sqrt(50)),
        ]

        for p1, p2, expected in cases:
            actual = core.p2p(p1, p2)
            self.assertClose(expected, actual)

    def test_p2l_method(self):
        cases = [
            (core.Point(0, 0), core.Segment(1, 1, 1, 1), np.sqrt(2)),
            (core.Point(2, 2), core.Segment(1, 1, 1, 1), np.sqrt(2)),

            # diagonal segment
            (core.Point(0, 0), core.Segment(1, 1, 2, 2), 0),
            (core.Point(1, 1), core.Segment(1, 1, 2, 2), 0),
            (core.Point(2, 2), core.Segment(1, 1, 2, 2), 0),
            (core.Point(3, 3), core.Segment(1, 1, 2, 2), 0),
            (core.Point(1, 0), core.Segment(1, 1, 2, 2), np.sqrt(2) / 2),
            (core.Point(2, 3), core.Segment(1, 1, 2, 2), np.sqrt(2) / 2),

            # vertical segment
            (core.Point(1, 0), core.Segment(1, 1, 1, 2), 0),
            (core.Point(1, 1), core.Segment(1, 1, 1, 2), 0),
            (core.Point(1, 2), core.Segment(1, 1, 1, 2), 0),
            (core.Point(1, 3), core.Segment(1, 1, 1, 2), 0),
            (core.Point(0, 0), core.Segment(1, 1, 1, 2), 1),
            (core.Point(2, 2), core.Segment(1, 1, 1, 2), 1),

            # horizontal segment
            (core.Point(0, 1), core.Segment(1, 1, 2, 1), 0),
            (core.Point(1, 1), core.Segment(1, 1, 2, 1), 0),
            (core.Point(2, 1), core.Segment(1, 1, 2, 1), 0),
            (core.Point(3, 1), core.Segment(1, 1, 2, 1), 0),
            (core.Point(0, 0), core.Segment(1, 1, 2, 1), 1),
            (core.Point(2, 2), core.Segment(1, 1, 2, 1), 1),
        ]

        for point, segment, expected in cases:
            actual = core.p2l(point, segment)
            self.assertClose(expected, actual)

    def test_p2s_method(self):
        cases = [
            # diagonal segment
            (core.Point(0, 0), core.Segment(1, 1, 2, 2), np.sqrt(2)),
            (core.Point(1, 1), core.Segment(1, 1, 2, 2), 0),
            (core.Point(2, 2), core.Segment(1, 1, 2, 2), 0),
            (core.Point(3, 3), core.Segment(1, 1, 2, 2), np.sqrt(2)),
            (core.Point(1, 0), core.Segment(1, 1, 2, 2), 1),
            (core.Point(2, 3), core.Segment(1, 1, 2, 2), 1),

            (core.Point(1, 3), core.Segment(1, 1, 3, 3), np.sqrt(8) / 2),
            (core.Point(3, 1), core.Segment(1, 1, 3, 3), np.sqrt(8) / 2),

            # vertical segment
            (core.Point(1, 0), core.Segment(1, 1, 1, 2), 1),
            (core.Point(1, 1), core.Segment(1, 1, 1, 2), 0),
            (core.Point(1, 2), core.Segment(1, 1, 1, 2), 0),
            (core.Point(1, 3), core.Segment(1, 1, 1, 2), 1),
            (core.Point(0, 0), core.Segment(1, 1, 1, 2), np.sqrt(2)),
            (core.Point(2, 3), core.Segment(1, 1, 1, 2), np.sqrt(2)),
            (core.Point(0, 2), core.Segment(1, 1, 1, 2), 1),
            (core.Point(2, 2), core.Segment(1, 1, 1, 2), 1),

            # # horizontal segment
            (core.Point(0, 1), core.Segment(1, 1, 2, 1), 1),
            (core.Point(1, 1), core.Segment(1, 1, 2, 1), 0),
            (core.Point(2, 1), core.Segment(1, 1, 2, 1), 0),
            (core.Point(3, 1), core.Segment(1, 1, 2, 1), 1),
            (core.Point(0, 0), core.Segment(1, 1, 2, 1), np.sqrt(2)),
            (core.Point(3, 2), core.Segment(1, 1, 2, 1), np.sqrt(2)),
            (core.Point(1, 2), core.Segment(1, 1, 2, 1), 1),
            (core.Point(1, 0), core.Segment(1, 1, 2, 1), 1),
        ]

        for point, segment, expected in cases:
            actual = core.p2s(point, segment)
            self.assertClose(expected, actual)

    def test_angle_method(self):
        cases = [
            (core.Segment(0, 0, 5, 0), core.Segment(0, 0, 5, 0), 0),
            (core.Segment(0, 0, 5, 5), core.Segment(0, 0, 5, 0), 45),
            (core.Segment(0, 0, 0, 5), core.Segment(0, 0, 5, 0), 90),
            (core.Segment(5, 0, 0, 0), core.Segment(0, 0, 5, 0), 180),
            (core.Segment(5, 5, 0, 0), core.Segment(0, 0, 5, 0), 225),
            (core.Segment(5, 5, 0, 0), core.Segment(0, 0, 0, 5), 135),
        ]

        for s1, s2, expected in cases:
            actual = core.angle(s1, s2)
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

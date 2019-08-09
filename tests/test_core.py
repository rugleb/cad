import unittest

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


class DrawStyleTestCase(unittest.TestCase):

    def test_on_types(self):
        for style in core.DrawStyle:
            self.assertIsInstance(style.width, float)
            self.assertIsInstance(style.color, core.Color)


if __name__ == '__main__':
    unittest.main()

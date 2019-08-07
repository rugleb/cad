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


class DrawStyleTestCase(unittest.TestCase):

    def test_on_types(self):
        for style in core.DrawStyle:
            self.assertIsInstance(style.width, float)
            self.assertIsInstance(style.color, core.Color)


if __name__ == '__main__':
    unittest.main()

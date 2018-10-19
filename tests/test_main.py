import unittest

from cad.main import isPointOnLine
from cad.drawing import Line, Point


class MainModuleTestCase(unittest.TestCase):

    def testIsPointOnLineMethod(self):
        line = Line(Point(10, 10), Point(100, 100))

        self.assertTrue(isPointOnLine(Point(10, 10), line))
        self.assertTrue(isPointOnLine(Point(50, 50), line))
        self.assertTrue(isPointOnLine(Point(100, 100), line))

        self.assertFalse(isPointOnLine(Point(9, 9), line))
        self.assertFalse(isPointOnLine(Point(51, 50), line))
        self.assertFalse(isPointOnLine(Point(101, 101), line))


if __name__ == '__main__':
    unittest.main()

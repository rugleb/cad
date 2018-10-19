import unittest
from math import sqrt

from cad.drawing import *


class DrawingTestCase(unittest.TestCase):

    def testDistancePointToPoint(self):
        d = distancePointToPoint(Point(0, 0), Point(10, 0))
        self.assertEqual(10., d)

        d = distancePointToPoint(Point(0, 0), Point(10, 10))
        self.assertEqual(10. * sqrt(2), d)

    def testDistancePointOnVector(self):
        line = Line(Point(10, 10), Point(20, 10))

        d = distancePointToVector(Point(10, 10), line)
        self.assertEqual(0., d)

        d = distancePointToVector(Point(15, 20), line)
        self.assertEqual(10., d)

        line = Line(Point(10, 10), Point(20, 20))
        d = distancePointToVector(Point(30, 30), line)
        self.assertEqual(0., d)


if __name__ == '__main__':
    unittest.main()

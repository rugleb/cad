import unittest
from math import sqrt

from cad.drawing import *


class DrawingTestCase(unittest.TestCase):

    def testDistancePointToPoint(self):
        d = distancePointToPoint(Point(0, 0), Point(10, 0))
        self.assertEqual(10., d)

        d = distancePointToPoint(Point(0, 0), Point(10, 10))
        self.assertEqual(10. * sqrt(2), d)


if __name__ == '__main__':
    unittest.main()

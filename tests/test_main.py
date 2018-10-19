import unittest
from PyQt5 import QtCore

from cad.main import isPointOnLine


class MainModuleTestCase(unittest.TestCase):

    def testIsPointOnLineMethod(self):
        p1 = QtCore.QPointF(10, 10)
        p2 = QtCore.QPointF(100, 100)
        line = QtCore.QLineF(p1, p2)

        self.assertTrue(isPointOnLine(QtCore.QPointF(10, 10), line))
        self.assertTrue(isPointOnLine(QtCore.QPointF(50, 50), line))
        self.assertTrue(isPointOnLine(QtCore.QPointF(100, 100), line))

        self.assertFalse(isPointOnLine(QtCore.QPointF(9, 9), line))
        self.assertFalse(isPointOnLine(QtCore.QPointF(51, 50), line))
        self.assertFalse(isPointOnLine(QtCore.QPointF(101, 101), line))


if __name__ == '__main__':
    unittest.main()

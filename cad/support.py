from PyQt5.QtCore import QPointF, QLineF

from cad.figures import Point, Line


def isPointable(obj):
    return type(obj) in (QPointF, Point)


def isLinable(obj):
    return type(obj) in (QLineF, Line)

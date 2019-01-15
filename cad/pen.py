from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

WIDTH = 5
COLOR = Qt.gray
STYLE = Qt.SolidLine

ACTIVE_WIDTH = 7
ACTIVE_COLOR = Qt.darkGray
ACTIVE_STYLE = STYLE

line = QPen(COLOR, WIDTH, STYLE)
point = QPen(line.color(), WIDTH * 2, line.style())

activeLine = QPen(ACTIVE_COLOR, ACTIVE_WIDTH, ACTIVE_STYLE)
activePoint = QPen(ACTIVE_COLOR, ACTIVE_WIDTH * 2, ACTIVE_STYLE)

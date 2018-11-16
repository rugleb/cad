from cad.figures import Line, Point


line1 = Line(Point(5, 5), Point(5, 10))
line2 = Line(Point(5, 5), Point(10, 5))


figures = [
    line1,
    line2,
]

relations = {}

for figure in figures:
    relations[figure] = figures.index(figure)

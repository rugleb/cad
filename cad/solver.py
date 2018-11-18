from time import time

from scipy import optimize
from sympy import Symbol, lambdify


class Point:
    def __init__(self, number: int, x: float, y: float):
        self.i = number
        self.x = x
        self.y = y

    def getEquations(self):
        x = Symbol('x{}'.format(self.i))
        y = Symbol('y{}'.format(self.i))
        return [
            x - self.x,
            y - self.y,
        ]


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def getEquations(self):
        equations = []
        for point in (self.p1, self.p2):
            equations.extend(point.getEquations())
        return equations


a = time()

p1 = Point(1, 5, 5)
p2 = Point(2, 10, 10)
p3 = Point(3, 20, 10)

l1 = Line(p2, p3)

system = []
for obj in (p1, l1):
    system.extend(obj.getEquations())

b = time()

functions = []
symbols = [
    Symbol('x1'),
    Symbol('y1'),
    Symbol('x2'),
    Symbol('y2'),
    Symbol('x3'),
    Symbol('y3'),
]

for equation in system:
    func = lambdify(symbols, equation)
    functions.append(func)

c = time()


def fun(x):
    return [f(*x) for f in functions]


d = time()

result = optimize.fsolve(fun, [0] * len(functions), xtol=0.01)

z = time()

pass

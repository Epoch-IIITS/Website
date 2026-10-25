r"""Reference solution for PY-26 Inheritance, Special Methods and Dataclasses.

`Shape` holds behaviour shared by every shape and defines comparison in terms of `area()`, which
each subclass overrides. `Square` only changes how it is constructed and its name. Returning
`NotImplemented` lets Python report a proper error for unsupported comparisons. The dataclass
generates the initialiser, representation and equality for `Point`.
"""
import math
from dataclasses import dataclass


class Shape:
    name = "shape"

    def area(self):
        raise NotImplementedError("subclasses must implement area")

    def describe(self):
        return f"{self.name} with area {self.area():.2f}"

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return abs(self.area() - other.area()) < 1e-9

    def __lt__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()


class Rectangle(Shape):
    name = "rectangle"

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Square(Rectangle):
    name = "square"

    def __init__(self, side):
        super().__init__(side, side)


class Circle(Shape):
    name = "circle"

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


def total_area(shapes):
    return sum(s.area() for s in shapes)


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

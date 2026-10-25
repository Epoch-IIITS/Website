import math
from dataclasses import dataclass


class Shape:
    name = "shape"

    def area(self):
        raise NotImplementedError("subclasses must implement area")

    def describe(self):
        return f"{self.name} with area {self.area():.2f}"


class Rectangle(Shape):
    name = "rectangle"

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# TODO: Shape.__eq__ / __lt__, Rectangle.perimeter, Square, Circle, total_area, Point

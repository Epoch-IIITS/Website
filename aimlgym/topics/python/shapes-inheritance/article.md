# Inheritance, Special Methods and Dataclasses

## Learning outcomes

After this lesson you can:

- Create subclasses that reuse and override base-class methods
- Call the parent initialiser with super()
- Implement special methods such as __eq__ and __lt__
- Generate boilerplate with @dataclass

## Intuition
Rectangles, squares and circles are all shapes: they all have an area and can describe
themselves. **Inheritance** lets you write the shared parts once in a base class and only the
differences in each subclass. A square is a rectangle with equal sides, so `Square` can inherit
almost everything from `Rectangle`.

## Precise explanation
```python
class Shape:
    name = "shape"
    def area(self):
        raise NotImplementedError("subclasses must implement area")
    def describe(self):                       # shared code, uses self.area()
        return f"{self.name} with area {self.area():.2f}"

class Rectangle(Shape):                       # Rectangle inherits from Shape
    name = "rectangle"
    def __init__(self, width, height):
        self.width, self.height = width, height
    def area(self):                           # overrides Shape.area
        return self.width * self.height

class Square(Rectangle):
    name = "square"
    def __init__(self, side):
        super().__init__(side, side)          # reuse the parent's initialiser
```
* Method lookup goes object → class → parent → ... (`Square` → `Rectangle` → `Shape`).
* `isinstance(Square(2), Rectangle)` is `True`. Code that calls `shape.area()` works for any
  subclass — this is **polymorphism**.
* **Special ("dunder") methods** customise operators: `__eq__` for `==`, `__lt__` for `<` (which
  makes `sorted` work), `__repr__` for display, `__add__` for `+`.
* `@dataclass` (from `dataclasses`) writes `__init__`, `__repr__` and `__eq__` from annotated
  fields:
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
Point(1, 2) == Point(1, 2)    # True; repr: Point(x=1, y=2)
```
`x: float` is a **type annotation**: documentation for readers and tools; Python does not convert
or check the value. (Pydantic, in FA-10, does check.)

## Worked example
`[Square(2), Circle(1)]` → `describe()` gives `"square with area 4.00"` and
`"circle with area 3.14"`; `sorted` with `__lt__` comparing areas puts the circle first.

## Common mistakes
* Forgetting `super().__init__(...)`, so parent attributes are never set.
* Defining `__eq__` but comparing different types; return `NotImplemented` for unknown types.
* Deep inheritance trees: prefer a shallow hierarchy and small classes.

## Why this matters
Deep-learning frameworks are built on inheritance (every layer subclasses a base `Module`), and
FastAPI request models subclass Pydantic's `BaseModel`.

## References

- [The Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html) — Python Software Foundation (`S046`)
- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html) — Python Software Foundation (`S057`)

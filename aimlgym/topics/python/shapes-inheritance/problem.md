# PY-26 · Inheritance, Special Methods and Dataclasses

**Topic:** Python · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** PY-25 Classes: A Bank Account

Read the lesson first: [article.md](article.md)

## Task

Implement:

* `Shape` with class attribute `name = "shape"`, `area()` raising `NotImplementedError`,
  `describe()` returning `f"{self.name} with area {self.area():.2f}"`, `__eq__` (shapes are equal
  when both are `Shape` objects and their areas differ by less than `1e-9`; otherwise return
  `NotImplemented`) and `__lt__` (compare areas).
* `Rectangle(width, height)` (`name = "rectangle"`), with `area()` and `perimeter()`.
* `Square(side)` (`name = "square"`) — a subclass of `Rectangle` that calls `super().__init__`.
* `Circle(radius)` (`name = "circle"`) using `math.pi`; `perimeter()` is the circumference.
* `total_area(shapes)` — sum of areas.
* `@dataclass class Point` with fields `x` and `y` and a method `distance_to(other)`.

**Examples**
```python
Square(2).describe()            # 'square with area 4.00'
Rectangle(1, 4) == Square(2)    # True — same area
sorted([Square(2), Circle(1)])  # [Circle(1), Square(2)] by area
Point(0, 0).distance_to(Point(3, 4))   # 5.0
```

## Hints

<details><summary>Hint 1</summary>

`class Square(Rectangle):` with `def __init__(self, side): super().__init__(side, side)`.

</details>

<details><summary>Hint 2</summary>

In `__eq__`, start with `if not isinstance(other, Shape): return NotImplemented`.

</details>

<details><summary>Hint 3</summary>

`@dataclass` above `class Point:` with `x: float` and `y: float`; use `math.hypot` for the distance.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_square_inherits` | Subclass `Rectangle` and call `super().__init__(side, side)`; set `name = "square"`. |
| `test_circle` | Use `math.pi * r ** 2` for the area and `2 * math.pi * r` for the perimeter. |
| `test_equality_and_sorting` | Define `__eq__` and `__lt__` on `Shape` using areas; return `NotImplemented` for non-shapes. |
| `test_point_dataclass` | Decorate `Point` with `@dataclass` and declare `x: float` and `y: float`. |
| `test_total_area` | Sum `s.area()` over the shapes; an empty list gives 0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`Shape` holds behaviour shared by every shape and defines comparison in terms of `area()`, which
each subclass overrides. `Square` only changes how it is constructed and its name. Returning
`NotImplemented` lets Python report a proper error for unsupported comparisons. The dataclass
generates the initialiser, representation and equality for `Point`.

## References

- [The Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html) — Python Software Foundation (`S046`)
- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html) — Python Software Foundation (`S057`)

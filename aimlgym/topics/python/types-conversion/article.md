# Types and Conversion

## Learning outcomes

After this lesson you can:

- Recognise int, float, str and bool values
- Inspect a value with type()
- Convert between types with int(), float(), str() and round()

## Intuition
`"3"` and `3` look alike on screen but are different kinds of value: one is text, the other a
number. Python must know the **type** of a value to know what operations mean: `"3" + "3"` is
`"33"`, while `3 + 3` is `6`.

## Precise explanation
| Type | Examples | Notes |
|---|---|---|
| `int` | `0`, `-7`, `2026` | whole numbers, any size |
| `float` | `3.5`, `0.1`, `2.0` | decimals, stored approximately |
| `str` | `"hi"`, `"19.99"` | text |
| `bool` | `True`, `False` | truth values |

* `type(x)` returns the type; `type(x).__name__` is its name as text, e.g. `"float"`.
* Conversions create a **new** value: `int("3")` → `3`, `float("19.99")` → `19.99`,
  `str(3)` → `"3"`, `int(3.9)` → `3` (truncates toward zero), `bool(0)` → `False`.
* `round(x, 2)` rounds to two decimal places.
* Mixing types: `int + float` gives a float; `str + int` is a `TypeError` — convert first.

## Worked example
```python
quantity_text = "3"
quantity = int(quantity_text)   # 3
label = str(quantity) + " items" # "3 items"
print(type(quantity).__name__)  # int
print(0.1 + 0.2)                # 0.30000000000000004  (floats are approximate)
print(round(0.1 + 0.2, 2))      # 0.3
```

## Common mistakes
* `int("19.99")` raises `ValueError`; use `float("19.99")` first.
* Comparing floats exactly; `0.1 + 0.2 == 0.3` is `False`. Round or compare with a tolerance.
* Expecting `int(2.7)` to round to 3 — it truncates to 2.

## Why this matters
Data read from files, forms and the keyboard always arrives as text. Converting it correctly is
the first step of every data pipeline, and dtype mistakes are a common source of ML bugs.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [Built-in Functions](https://docs.python.org/3/library/functions.html) — Python Software Foundation (`S048`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)

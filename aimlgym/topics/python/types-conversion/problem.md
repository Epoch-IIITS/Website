# PY-03 · Types and Conversion

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-02 Variables and f-strings

Read the lesson first: [article.md](article.md)

## Task

The starter defines three text values that came from a form:

```python
price_text = "19.99"
quantity_text = "3"
discount_text = "0.1"
```

Create:
* `price` — `price_text` as a `float`
* `quantity` — `quantity_text` as an `int`
* `discount` — `discount_text` as a `float`
* `total` — `price * quantity * (1 - discount)`
* `total_rounded` — `total` rounded to 2 decimal places
* `label` — the text `"3 items"`, built with `str(quantity) + " items"`

Then print exactly:
```
Total: 53.97
price is float
quantity is int
3 items
```
Use `type(...).__name__` for lines 2 and 3.

## Hints

<details><summary>Hint 1</summary>

`price = float(price_text)` and `quantity = int(quantity_text)`.

</details>

<details><summary>Hint 2</summary>

`total_rounded = round(total, 2)`; print it with an f-string.

</details>

<details><summary>Hint 3</summary>

`print(f"price is {type(price).__name__}")` prints the type's name.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_price_float` | Use `float(price_text)`; `int` cannot parse `"19.99"`. |
| `test_quantity_int` | Use `int(quantity_text)` so quantity is a whole number. |
| `test_total` | Multiply by `(1 - discount)` and round only `total_rounded`, not `total`. |
| `test_label` | Convert with `str(quantity)` before adding `" items"`. |
| `test_output` | Print `total_rounded`, then the two type names from `type(x).__name__`, then the label. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each text is converted with the function for its target type. The total is computed with
floats, then rounded only for display, so `total` keeps full precision. `str(quantity)` turns
the number back into text before it is joined with `" items"`.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [Built-in Functions](https://docs.python.org/3/library/functions.html) — Python Software Foundation (`S048`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)

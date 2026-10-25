# Variables and f-strings

## Learning outcomes

After this lesson you can:

- Create and reassign variables
- Choose readable snake_case names
- Do simple arithmetic with + - * /
- Insert values into text with f-strings

## Intuition
A variable is a name tag attached to a value. `age = 19` means "from now on, `age` refers to
19". You can later move the tag to a different value: `age = 20`.

## Precise explanation
```python
name = "Ada"          # a string
age = 19              # a whole number (int)
height_m = 1.68       # a decimal number (float)
is_student = True     # a truth value (bool): True or False
next_age = age + 1    # the right side is computed first, then stored: 20
```
* `=` is **assignment**, not "equals". The right-hand side is evaluated, then the name on the
  left is bound to the result.
* Names may contain letters, digits and `_`, cannot start with a digit, and are case-sensitive
  (`Age` and `age` are different). Python style uses `snake_case`.
* Python works as a calculator: `+ - * /` add, subtract, multiply and divide. `/` always gives
  a float: `7 / 2` is `3.5`. (More operators come in PY-05.)
* An **f-string** inserts values into text: `f"Name: {name}"` → `Name: Ada`. Any expression can
  go inside the braces: `f"{age + 1}"` → `20`.

## Worked example
```python
price = 4
count = 3
total = price * count
print(f"{count} items cost {total}")   # 3 items cost 12
count = 5                              # reassignment
print(f"{count} items cost {total}")   # 5 items cost 12 — total was computed earlier!
```

## Common mistakes
* Using a variable before assigning it → `NameError`.
* Expecting `total` to update automatically when `count` changes; it stores a value, not a formula.
* Forgetting the `f` before the quotes: `"Name: {name}"` prints the braces literally.
* Writing `"Age: " + age` — you cannot add a string and an int (see PY-03).

## Why this matters
Every model, dataset and hyperparameter in later topics lives in a variable. Clear names such as
`learning_rate` instead of `x` make code readable.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)

# Functions, Strings and f-strings

## Learning outcomes

After this lesson you can:

- Define a function with a default argument
- Use str.strip and f-strings
- Return a value instead of printing it

## Intuition
A function is a named recipe: you give it ingredients (arguments) and it hands back a result
(the return value). Most bugs in beginner code come from mixing up *printing* something with
*returning* it. Printing shows text to a human; returning gives a value to the rest of the
program — and to the automatic tests.

## Precise explanation
```python
def greet(name="World"):
    return f"Hello, {name}!"
```
* `def` creates a function object and binds it to the name `greet`.
* `name="World"` is a **default argument**: if the caller passes nothing, `name` is `"World"`.
* An **f-string** (`f"..."`) evaluates every `{expression}` inside it and inserts the result.
* `return` ends the function and sends the value back to the caller. A function with no
  `return` returns `None`.

Useful string methods: `s.strip()` removes leading/trailing whitespace; `s.title()`
capitalises each word; `s.lower()` / `s.upper()` change case. Strings are **immutable** — each
method returns a *new* string and leaves the original unchanged.

## Worked example
```python
>>> raw = "   ada lovelace  "
>>> clean = raw.strip()        # 'ada lovelace'
>>> clean.title()              # 'Ada Lovelace'
>>> f"Hello, {clean.title()}!"
'Hello, Ada Lovelace!'
>>> raw                        # unchanged
'   ada lovelace  '
```

## Common mistakes
* Using `print(...)` inside the function and forgetting `return` → the caller receives `None`.
* Writing `raw.strip()` on its own line and expecting `raw` to change (strings are immutable).
* Forgetting the `f` prefix, which produces the literal text `{name}`.
* Using a mutable default such as `def f(x=[])` — the same list is shared between calls.

## Why this matters
Every later exercise — from a NumPy helper to an agent tool — is a function whose *return
value* is checked. Clean input normalisation (strip, lower) is also the first step of every
text-processing pipeline in NLP.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
- [Learn Python - Interactive Course](https://aqemery.github.io/learn-python/) — aqemery (GitHub user) (`S005`)

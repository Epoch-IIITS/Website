# Functions as Values

## Learning outcomes

After this lesson you can:

- Pass functions as arguments and return them from functions
- Write lambda expressions and sort with key=
- Accept *args, **kwargs and keyword-only parameters
- Write a simple decorator with functools.wraps

## Intuition
In Python a function is a value like a number or a list. You can store it in a variable, pass
it to another function ("sort these words *using this rule*"), or build a new function from old
ones. This is how sorting keys, callbacks, tool registries and decorators work.

## Precise explanation
**Passing and returning functions**
```python
def apply_twice(f, x):
    return f(f(x))

def make_adder(n):
    def add(x):          # a nested function "remembers" n: a closure
        return x + n
    return add

apply_twice(make_adder(3), 10)   # 16
```
**lambda** creates a small unnamed function from one expression:
`square = lambda x: x * x`. It is most useful as a `key`:
`sorted(words, key=lambda w: (len(w), w))` sorts by length, then alphabetically.

**Flexible parameters**
```python
def report(name, *scores, sep=", ", **extra):
    # scores is a tuple of extra positional arguments
    # sep is keyword-only because it comes after *scores
    # extra is a dict of extra keyword arguments
```
`report("ada", 90, 85, sep="/", club="ai")` → `scores == (90, 85)`,
`extra == {"club": "ai"}`. Calling with `*list` or `**dict` unpacks them into arguments.

**Decorators** wrap a function to add behaviour. `@count_calls` above `def f` means
`f = count_calls(f)`.
```python
import functools

def count_calls(func):
    @functools.wraps(func)        # keep func's name and docstring
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
```

## Worked example
`pipeline(str.strip, str.lower)("  Hi ")` applies `strip` then `lower` → `"hi"`.

## Common mistakes
* Calling instead of passing: `sorted(words, key=len())` is an error; pass `len`.
* Mutable default arguments: `def f(x, seen=[])` shares one list across calls.
* Forgetting to `return` the wrapper (or the wrapped function's result) in a decorator.
* Putting a keyword-only parameter before `*args` and expecting it to collect a positional value.

## Why this matters
`key=` functions sort model results, callbacks drive training loops, and agent tool registries
(AG-01) register Python functions with a decorator and call them with `**arguments`.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
- [Built-in Functions](https://docs.python.org/3/library/functions.html) — Python Software Foundation (`S048`)
- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)

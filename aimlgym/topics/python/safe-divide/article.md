# Handling Exceptions Deliberately

## Learning outcomes

After this lesson you can:

- Catch specific exceptions with try/except
- Distinguish recoverable and unrecoverable errors
- Process a batch while recording failures

## Intuition
Some errors are expected and recoverable (dividing by zero in a ratio where "undefined" is a
fine answer); others signal a bug (passing a string where a number belongs). Good code catches
the first kind *specifically* and lets the second kind surface.

## Precise explanation
```python
try:
    result = a / b
except ZeroDivisionError:
    result = None
```
* Code in `try` runs; if an exception is raised, Python looks for a matching `except`.
* Catch the **narrowest** exception you can handle. A bare `except:` or `except Exception:`
  also swallows typos (`NameError`) and type bugs, hiding real problems.
* `else:` runs only if no exception occurred; `finally:` always runs.
* Division by zero: `1 / 0` raises `ZeroDivisionError`, and so does `1.0 / 0.0` in plain Python
  (NumPy instead returns `inf` with a warning).

**Batch processing pattern:** process each item, store the result or a marker, and keep a list
of the indices that failed — one bad record should not abort a whole dataset.

## Worked example
`divide_pairs([(6, 3), (1, 0), (5, 2)])` → results `[2.0, None, 2.5]`, failed indices `[1]`.

## Common mistakes
* `except:` with no type → hides `TypeError` from `safe_divide("6", 3)`.
* Checking `if b == 0` only — fine for numbers, but the exercise asks you to practise exceptions.
* Returning the error message string as the result, mixing types in the output list.

## Why this matters
Data loaders, tool-calling agents (AG-15) and federated clients that drop out (FL topics) all
need the same skill: recover from expected failures, record them, continue.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)

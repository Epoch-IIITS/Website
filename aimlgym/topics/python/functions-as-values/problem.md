# PY-17 · Functions as Values

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-16 Unique Words in Order

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `pipeline(*funcs)` → returns a new function `run(x)` that applies each function in `funcs` in
   order and returns the final value. With no functions, `run(x)` returns `x`.
2. `sort_words(words)` → a new list sorted by length, then alphabetically (use `sorted` with a
   `lambda` key).
3. `format_record(name, *scores, sep=", ", **extra)` → a string:
   `"<name>: <scores joined by sep>"`, followed — if `extra` is not empty — by `" | "` and the
   extra items as `key=value`, sorted by key and joined by `", "`.
   With no scores the part after the colon is empty: `"ada: "`.
4. `count_calls(func)` → a decorator. The returned wrapper calls `func` with the same
   arguments, returns its result, has an attribute `calls` counting how many times it was
   called, and keeps `func`'s `__name__` (use `functools.wraps`).

**Examples**
```python
pipeline(str.strip, str.upper)("  hi ")             # 'HI'
sort_words(["pear", "fig", "apple", "kiwi"])        # ['fig', 'kiwi', 'pear', 'apple']
format_record("ada", 90, 85)                       # 'ada: 90, 85'
format_record("bob", 70, sep="/", year=2, club="ai")  # 'bob: 70 | club=ai, year=2'
```

## Hints

<details><summary>Hint 1</summary>

Inside `run`, loop `for f in funcs: x = f(x)`, then return x.

</details>

<details><summary>Hint 2</summary>

`key=lambda w: (len(w), w)`; build the score text with `sep.join(str(s) for s in scores)`.

</details>

<details><summary>Hint 3</summary>

For extras: `", ".join(f"{k}={v}" for k, v in sorted(extra.items()))`. For the decorator, copy the pattern from the lesson.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_pipeline_order` | Apply the functions left to right, feeding each result into the next. |
| `test_sort_words` | Use `sorted` (it returns a new list) with a tuple key `(len(w), w)`. |
| `test_format_extra_sorted` | Sort `extra.items()` by key and join scores with the given `sep`. |
| `test_count_calls` | Initialise `wrapper.calls = 0` and increment it inside the wrapper; return func's result. |
| `test_wraps_keeps_name` | Decorate the wrapper with `@functools.wraps(func)`. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`pipeline` returns a closure that remembers `funcs`. The sort key is a tuple, so ties in length
fall back to alphabetical order. `format_record` treats `*scores` as a tuple and `**extra` as a
dict, sorting the latter so the output is deterministic. The decorator stores its counter on the
wrapper itself and forwards every argument with `*args, **kwargs`.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
- [Built-in Functions](https://docs.python.org/3/library/functions.html) — Python Software Foundation (`S048`)
- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)

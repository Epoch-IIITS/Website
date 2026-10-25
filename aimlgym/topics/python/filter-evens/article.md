# Filtering with List Comprehensions

## Learning outcomes

After this lesson you can:

- Use the modulo operator
- Write a list comprehension with a condition
- Preserve order while filtering

## Intuition
Filtering means keeping the items that pass a test. In Python the most readable filter is a
**list comprehension**: "give me `x` for each `x` in `nums` if `x` is even".

## Precise explanation
`a % b` is the remainder of `a` divided by `b`. An integer `x` is even exactly when
`x % 2 == 0`. In Python `%` always returns a result with the sign of the divisor, so
`-4 % 2 == 0` and `-3 % 2 == 1`: the test works for negative numbers too.

```python
[x for x in nums if x % 2 == 0]
```
is equivalent to
```python
out = []
for x in nums:
    if x % 2 == 0:
        out.append(x)
```
Both keep the original order and build a **new** list.

## Worked example
`nums = [5, -4, 0, 7, 12]` → test each: 5%2=1 ✗, -4%2=0 ✓, 0%2=0 ✓, 7%2=1 ✗, 12%2=0 ✓ →
`[-4, 0, 12]`.

## Common mistakes
* Testing `x % 2 == 1` for "odd" and then negating incorrectly; just test `== 0`.
* Removing items from a list while looping over it — skips elements. Build a new list instead.
* Forgetting that `0` is even.

## Why this matters
Boolean filtering is the same idea as NumPy masks (`a[a % 2 == 0]`) and pandas row selection
(`df[df.score > 50]`), which you will use constantly.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)

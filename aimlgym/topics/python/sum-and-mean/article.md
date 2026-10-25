# The Accumulator Pattern

## Learning outcomes

After this lesson you can:

- Accumulate values in a loop
- Handle the empty-input edge case
- Return a tuple of results

## Intuition
To add up a column of numbers by hand you keep a running total and update it once per number.
In code this is the **accumulator pattern**: start a variable at a neutral value, then update it
inside a loop.

## Precise explanation
```python
total = 0            # neutral element for addition
for x in nums:
    total += x       # same as total = total + x
```
The mean (arithmetic average) of $n$ numbers is

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i.$$

It is undefined when $n = 0$, so code must decide what to do with an empty list. Here we return
`None` for the mean (the sum of an empty list is still `0`).

A function can return several values as a **tuple**: `return total, mean` returns
`(total, mean)`, which the caller can unpack: `t, m = sum_and_mean(data)`.

Python also provides `sum(nums)` and `statistics.mean(nums)`; the latter raises
`StatisticsError` on empty input. Writing the loop yourself once makes clear what those helpers do.

## Worked example
For `[2, 4, 9]`: total goes 0 → 2 → 6 → 15; n = 3; mean = 15 / 3 = 5.0.

## Common mistakes
* Dividing by `len(nums)` without checking for zero → `ZeroDivisionError`.
* Initialising `total = nums[0]` → crashes on an empty list and double-counts if you then loop
  over all items.
* Using `//` (floor division) instead of `/` → `7 // 2 == 3`, not `3.5`.

## Why this matters
Means appear everywhere: average loss per batch, average reward per episode, feature
standardisation. The empty-input edge case is the classic source of crashes in data pipelines.

## Library implementation

Python's built-in `sum(nums)` performs the same accumulation, and `statistics.fmean(nums)`
computes the mean (it raises `StatisticsError` for empty data instead of returning `None`).
You will import modules properly in PY-15; the comparison below already uses them.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)

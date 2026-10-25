# Loop State and Tuple Assignment

## Learning outcomes

After this lesson you can:

- Maintain state across loop iterations
- Use tuple assignment
- Handle small-n boundary cases

## Intuition
Each Fibonacci number is the sum of the previous two: 0, 1, 1, 2, 3, 5, 8, … To generate them
you only need to remember the *last two* values — a sliding window of state.

## Precise explanation
$F_0 = 0,\; F_1 = 1,\; F_k = F_{k-1} + F_{k-2}$ for $k \ge 2$.

**Tuple assignment** evaluates the whole right-hand side first, then assigns:
```python
a, b = 0, 1
for _ in range(n):
    out.append(a)
    a, b = b, a + b    # new a = old b, new b = old a + old b
```
Without tuple assignment you would need a temporary variable (`t = a + b; a = b; b = t`).
Writing `a = b` then `b = a + b` is a bug: `a` has already changed.

`_` is a conventional name for a loop variable you don't use.

## Worked example (n = 6)
| step | append a | (a, b) after |
|---|---|---|
| 1 | 0 | (1, 1) |
| 2 | 1 | (1, 2) |
| 3 | 1 | (2, 3) |
| 4 | 2 | (3, 5) |
| 5 | 3 | (5, 8) |
| 6 | 5 | (8, 13) |

Result: `[0, 1, 1, 2, 3, 5]`.

## Common mistakes
* Naive recursion `fib(k-1) + fib(k-2)` — exponential time; n = 40 takes seconds.
* Special-casing n = 1 and n = 2 with hard-coded lists and getting n = 0 wrong.
* Sequential (not simultaneous) assignment, as described above.

## Why this matters
Carrying a small amount of state through a loop is the core of running averages, momentum in
optimizers (DL-14) and discounted returns in RL (RL-01).

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)

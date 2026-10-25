# MA-01 · Summation and Product Notation

**Topic:** Mathematics for AI/ML · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-17 Functions as Values

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `summation(f, start, stop)` — $\sum_{i=start}^{stop} f(i)$ with a loop (0 if `stop < start`).
2. `product(f, start, stop)` — $\prod_{i=start}^{stop} f(i)$ with a loop (1 if `stop < start`).
3. `mean(xs)` — $\frac1n\sum x_i$ using your `summation` over indices; raise `ValueError` for an
   empty list.
4. `sum_of_squares(n)` — the closed form $n(n+1)(2n+1)/6$ as an `int`.
5. `accurate_sum(xs)` — the sum computed with `math.fsum`.

**Examples**
```python
summation(lambda i: 2 * i + 1, 1, 4)   # 24
product(lambda i: i, 1, 5)             # 120
mean([2, 4, 9])                        # 5.0
sum_of_squares(3)                      # 14
accurate_sum([0.1] * 10)               # 1.0
```

## Hints

<details><summary>Hint 1</summary>

`for i in range(start, stop + 1): total += f(i)` — note the `+ 1`.

</details>

<details><summary>Hint 2</summary>

A product starts from 1. For the mean, `summation(lambda i: xs[i], 0, len(xs) - 1) / len(xs)`.

</details>

<details><summary>Hint 3</summary>

`n * (n + 1) * (2 * n + 1) // 6` is exact because the product is always divisible by 6.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_sum_odd_numbers` | Include the last index: loop over `range(start, stop + 1)`. |
| `test_empty_ranges` | Start the sum at 0 and the product at 1; an empty range leaves them unchanged. |
| `test_mean` | Divide the sum by the number of items and raise ValueError for an empty list. |
| `test_closed_form_matches_loop` | Use `n * (n + 1) * (2 * n + 1) // 6`. |
| `test_accurate_sum` | Return `math.fsum(xs)`. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Σ and Π become loops over `range(start, stop + 1)` starting from their identity elements 0 and
1, which also gives the correct empty results. The mean reuses `summation` over list indices.
The closed form uses integer arithmetic on the full product before dividing, and `math.fsum`
compensates for rounding errors that a plain loop accumulates.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)

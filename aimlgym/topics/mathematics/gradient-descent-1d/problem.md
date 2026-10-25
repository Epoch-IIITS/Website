# MA-13 · Gradient Descent in 1D

**Topic:** Mathematics for AI/ML · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** MA-11 Derivative Rules and the Chain Rule

Read the lesson first: [article.md](article.md)

## Task

Write `gradient_descent(df, x0, lr, max_steps=1000, tol=1e-8)`.

* `df` is the derivative function. Update `x = x - lr * df(x)`.
* Stop when `abs(step) < tol` (after applying that step) or after `max_steps` updates.
* Return `(x, history)` where `history` lists every iterate **including** `x0`.
* Raise `ValueError` if `lr <= 0` or `max_steps < 1`.
* If `x` becomes non-finite (inf/nan), stop and return immediately.

**Examples**
```python
x, h = gradient_descent(lambda x: 2*(x-3), 0.0, 0.25)
# x ≈ 3.0; h[:4] == [0.0, 1.5, 2.25, 2.625]
x, h = gradient_descent(lambda x: 2*(x-3), 0.0, 1.5, max_steps=5)
# diverges: len(h) == 6 and |x - 3| grows each step
```

## Hints

<details><summary>Hint 1</summary>

Validate `lr` and `max_steps` first.

</details>

<details><summary>Hint 2</summary>

In the loop: `step = lr * df(x)`, `x = x - step`, append `x`.

</details>

<details><summary>Hint 3</summary>

Break when `abs(step) < tol` or `not math.isfinite(x)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_first_iterates` | Update with x − lr·df(x) (minus sign) and include x0 in history. |
| `test_already_at_min` | When the first step is 0 you should stop after one update. |
| `test_max_steps_respected` | history has max_steps + 1 entries when the cap is hit. |
| `test_nonfinite_stops` | Use math.isfinite to stop on overflow. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each iteration computes the step from the current slope, moves against it, and records the new
point. The loop ends on a tiny step (converged), a non-finite value (diverged) or the step cap,
so it always terminates.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

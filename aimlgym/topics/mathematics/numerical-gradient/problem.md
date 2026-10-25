# MA-14 · Numerical Gradient of f(x1..xn)

**Topic:** Mathematics for AI/ML · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** MA-10 Numerical Derivative (Central Difference), MA-13 Gradient Descent in 1D

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `numerical_gradient(f, x, h=1e-5)` — `f` takes a list of floats and returns a float; `x` is a
  list. Return a list of central-difference partial derivatives. Do **not** modify `x`.
* `gd_step(f, x, lr)` — return a new list `x - lr * grad`.

Raise `ValueError` if `h <= 0`.

**Examples**
```python
f = lambda v: v[0]**2 + 3*v[0]*v[1]
numerical_gradient(f, [1.0, 2.0])     # ≈ [8.0, 3.0]
gd_step(lambda v: v[0]**2 + v[1]**2, [1.0, -2.0], 0.25)   # ≈ [0.5, -1.0]
```

## Hints

<details><summary>Hint 1</summary>

For each i, copy x: `xp = list(x); xp[i] += h` and similarly `xm`.

</details>

<details><summary>Hint 2</summary>

Partial i is `(f(xp) - f(xm)) / (2 * h)`.

</details>

<details><summary>Hint 3</summary>

`gd_step`: `[xi - lr * gi for xi, gi in zip(x, grad)]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_not_modified` | Copy x before perturbing each coordinate. |
| `test_example` | Perturb only coordinate i; keep the others at their original values. |
| `test_gd_step` | Subtract lr times each gradient component. |
| `test_gd_converges` | gd_step must return a new list using the gradient at the current point. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each partial derivative perturbs a fresh copy of x along one axis in both directions, so x itself
is never changed. `gd_step` combines the gradient with the descent update element-wise.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)

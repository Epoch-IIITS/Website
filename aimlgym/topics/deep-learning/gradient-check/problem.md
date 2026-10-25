# DL-13 · Gradient Checking by Hand

**Topic:** Deep Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** DL-11 Backpropagation Through a Dense Layer, MA-14 Numerical Gradient of f(x1..xn)

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `relative_error(a, b)` → element-wise array (or float for scalars) using the formula with
  floor `1e-12`.
* `grad_check(f, grad, x, h=1e-5)` → dict `{"max_rel_error": float, "worst_index": tuple,
  "numerical": array}` where `f(x)` returns a float, `grad(x)` an array shaped like `x`, and `x` is a
  float array of any shape (must not be modified).

**Example**
```python
r = grad_check(lambda v: float((v**2).sum()), lambda v: 2*v, np.array([1., -2.]))
r["max_rel_error"] < 1e-8      # True
r = grad_check(lambda v: float((v**2).sum()), lambda v: v, np.array([1., -2.]))
round(r["max_rel_error"], 3)   # 0.333
```

## Hints

<details><summary>Hint 1</summary>

`np.abs(a - b) / np.maximum(np.abs(a) + np.abs(b), 1e-12)`.

</details>

<details><summary>Hint 2</summary>

Iterate with `np.ndindex(x.shape)`; perturb a copy of x at that index.

</details>

<details><summary>Hint 3</summary>

`worst = np.unravel_index(np.argmax(rel), x.shape)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_rel_error` | Floor the denominator at 1e-12 so 0 vs 0 gives 0. |
| `test_worst_index_2d` | Support any shape with np.ndindex and report a tuple index. |
| `test_no_mutation` | Perturb copies of x, never x itself. |
| `test_buggy` | Relative error = |a − b| / (|a| + |b|). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Every coordinate is perturbed on fresh copies, giving a central-difference gradient of any shape.
The relative error compares it with the analytic gradient in a scale-free way, and the worst
coordinate is reported to help locate bugs.

## References

- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

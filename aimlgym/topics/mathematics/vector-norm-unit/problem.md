# MA-05 · Vector Norm and Unit Vector

**Topic:** Mathematics for AI/ML · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** MA-04 Dot Product

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `norm(v, p=2)` for `p` in `{1, 2, float("inf")}`; raise `ValueError` for any other `p`.
  The norm of an empty vector is `0.0`.
* `unit(v)` returning a new list `v / ‖v‖₂`; raise `ValueError` for a zero (or empty) vector.

**Examples**
```python
norm([3, -4])               # 5.0
norm([3, -4], p=1)          # 7.0
norm([3, -4], p=float("inf"))  # 4.0
unit([3, -4])               # [0.6, -0.8]
unit([0, 0])                # raises ValueError
```

## Hints

<details><summary>Hint 1</summary>

L1: `sum(abs(x) for x in v)`; L∞: `max(abs(x) for x in v)` (watch the empty case).

</details>

<details><summary>Hint 2</summary>

L2: `math.sqrt(sum(x * x for x in v))`.

</details>

<details><summary>Hint 3</summary>

In `unit`, compute `n = norm(v)` once and raise if `n == 0`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_linf` | Take the maximum of absolute values, not of raw values. |
| `test_l1` | Use abs() on each element. |
| `test_unit_zero` | Raise ValueError before dividing by a zero norm. |
| `test_empty` | Return 0.0 for an empty vector (max() of an empty list raises). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each norm is a direct translation of its formula. The empty-vector branch returns 0.0 for
valid `p` (avoiding `max()` of an empty sequence) and falls through to the final `raise` for an
invalid `p`. `unit` reuses the L2 norm and refuses to divide by zero.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)

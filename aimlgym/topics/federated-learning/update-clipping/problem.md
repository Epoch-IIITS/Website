# FL-09 · Clipping Client Updates

**Topic:** Federated Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** FL-03 Client Updates as Deltas

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `clip_update(delta, max_norm)` → clipped new array; raise `ValueError` if `max_norm <= 0`.
* `clip_all(deltas, max_norm)` → `(clipped_list, n_clipped)` where `n_clipped` counts updates whose
  norm exceeded `max_norm`.

**Example**
```python
clip_update(np.array([3., 4.]), 2.5)     # [1.5, 2. ]
clip_all([np.array([3., 4.]), np.array([0.3, 0.4])], 2.5)[1]   # 1
```

## Hints

<details><summary>Hint 1</summary>

`n = np.linalg.norm(delta)`.

</details>

<details><summary>Hint 2</summary>

Scale factor `min(1.0, max_norm / n)` when `n > 0`.

</details>

<details><summary>Hint 3</summary>

Count with `sum(np.linalg.norm(d) > max_norm for d in deltas)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_clip` | Scale by max_norm / ‖Δ‖ when the norm is too large. |
| `test_norm_and_direction` | Scale the whole vector; don't clip coordinates independently. |
| `test_zero` | The zero vector must stay zero without dividing by zero. |
| `test_clip_all` | Count updates with norm strictly greater than max_norm. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Updates inside the ball are returned unchanged (as copies); larger ones are rescaled to lie exactly
on the sphere of radius max_norm, preserving direction. The zero vector falls in the first branch,
avoiding division by zero.

## References

- [Learning Differentially Private Recurrent Language Models](https://arxiv.org/abs/1710.06963) — H. Brendan McMahan, Daniel Ramage, Kunal Talwar, Li Zhang (`S031`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)

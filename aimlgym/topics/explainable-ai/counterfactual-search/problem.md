# XA-13 · Minimal Counterfactual Search

**Topic:** Explainable AI · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** XA-03 Tracing a Decision Path

Read the lesson first: [article.md](article.md)

## Task

Write `find_counterfactual(predict, x, steps, max_steps=3, lower=None, upper=None)` returning `None`
if no counterfactual exists within the search space, else a dict
`{"x_cf": array, "k": tuple[int], "cost": int, "label": label}`.
* Enumerate all `k` with `k_j = 0` for features whose step is 0 and `|k_j| <= max_steps` otherwise
  (`itertools.product`); skip candidates outside `[lower, upper]` (element-wise, if given).
* Choose minimal cost, ties → smallest `k` tuple (Python ordering). Evaluate candidates in batches or
  one by one (both fine).

**Example**
```python
predict = lambda X: (X[:, 0] + 2 * X[:, 1] >= 10).astype(int)
find_counterfactual(predict, np.array([4., 2.]), np.array([1., 1.]))
# {'x_cf': array([4., 3.]), 'k': (0, 1), 'cost': 1, 'label': 1}
```

## Hints

<details><summary>Hint 1</summary>

Original label: `c = predict(x[None])[0]`.

</details>

<details><summary>Hint 2</summary>

Ranges: `range(-max_steps, max_steps + 1)` if step != 0 else `(0,)`; build all k with `product`.

</details>

<details><summary>Hint 3</summary>

Sort candidates by `(sum(abs(k)), k)` and return the first that flips the label and is in bounds.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Sort candidates by (cost, k) and return the first that flips the label. |
| `test_immutable` | Features with step 0 must never change. |
| `test_bounds` | Skip candidates outside lower/upper. |
| `test_none` | Return None if no candidate within max_steps changes the prediction. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All step combinations are generated (immutable features fixed at 0), sorted by cost and then
lexicographically, and evaluated in one batch. The first in-bounds candidate whose predicted label
differs from the original is, by construction, a minimum-cost counterfactual.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)

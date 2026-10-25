# XA-03 · Tracing a Decision Path

**Topic:** Explainable AI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** ML-21 Decision Stump with Gini Impurity

Read the lesson first: [article.md](article.md)

## Task

Write `predict_with_path(tree, x, feature_names)` returning `(value, path)` where `path` is a list of
strings `"<name> <= <t>"` or `"<name> > <t>"` (threshold formatted with `str(t)`). Raise `ValueError`
if a node is malformed (neither a leaf nor a valid internal node).

**Example**
```python
tree = {"feature": 0, "threshold": 30, "left": {"feature": 1, "threshold": 5,
        "left": {"value": "approve"}, "right": {"value": "reject"}}, "right": {"value": "approve"}}
predict_with_path(tree, [25, 8], ["income", "debt"])
# ('reject', ['income <= 30', 'debt > 5'])
```

## Hints

<details><summary>Hint 1</summary>

Loop `while 'value' not in node`.

</details>

<details><summary>Hint 2</summary>

Compare `x[node['feature']] <= node['threshold']`.

</details>

<details><summary>Hint 3</summary>

Append `f"{name} <= {t}"` or `f"{name} > {t}"` then move to the child.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_boundary_left` | Go left when x_j <= threshold (inclusive). |
| `test_right_branch` | Right-branch conditions read 'name > t'. |
| `test_malformed` | Raise ValueError when a node lacks feature/threshold/left/right and isn't a leaf. |
| `test_leaf_root` | A tree that is just a leaf has an empty path. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The loop walks from the root to a leaf, recording the condition satisfied at each internal node
using the same `<=` convention as training. The leaf's value is the prediction.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)

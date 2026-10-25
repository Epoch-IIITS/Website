# CV-24 · Non-Maximum Suppression

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** CV-23 Intersection over Union

Read the lesson first: [article.md](article.md)

## Task

Write `nms(boxes, scores, iou_threshold=0.5, score_threshold=0.0)` returning a list of kept indices
(ints) following the algorithm above. Boxes are `(n, 4)` `[x1, y1, x2, y2]`. Raise `ValueError` if
`len(scores) != len(boxes)`.

**Example**
```python
boxes = np.array([[0, 0, 2, 2], [0.1, 0, 2.1, 2], [5, 5, 6, 6]])
nms(boxes, np.array([0.9, 0.8, 0.7]))   # [0, 2]
```

## Hints

<details><summary>Hint 1</summary>

Order: `idx = np.argsort(-scores, kind='stable')`, then filter by score threshold.

</details>

<details><summary>Hint 2</summary>

Write an `_iou(box, many)` helper (or reuse CV-23).

</details>

<details><summary>Hint 3</summary>

Loop: `i = order[0]`; keep it; `order = order[1:][iou(boxes[i], boxes[order[1:]]) <= t]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_chain` | Compare remaining boxes with each newly kept box, not only with the first box. |
| `test_order_by_score` | Return indices in the order they were kept (descending score). |
| `test_score_threshold` | Drop boxes below score_threshold before suppression. |
| `test_ties_lower_index` | Use a stable sort so equal scores keep the lower index first. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Candidates are processed in descending score order. Each iteration keeps the best remaining box
and filters out the rest that overlap it beyond the threshold, so every kept box suppresses its
own duplicates.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

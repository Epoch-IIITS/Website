# CV-23 · Intersection over Union

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** CV-01 Images as Arrays, NP-07 Centering Columns with Broadcasting

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `box_area(boxes)` → areas of `(n, 4)` boxes; raise `ValueError` if any box has `x2 <= x1` or
  `y2 <= y1`.
* `iou_matrix(A, B)` → `(m, n)` IoU matrix (vectorised).

**Example**
```python
iou_matrix(np.array([[0, 0, 2, 2]]), np.array([[1, 1, 3, 3], [5, 5, 6, 6], [0, 0, 2, 2]]))
# [[0.142857, 0.0, 1.0]]
```

## Hints

<details><summary>Hint 1</summary>

`(b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])`.

</details>

<details><summary>Hint 2</summary>

`ix1 = np.maximum(A[:, None, 0], B[None, :, 0])` … `iw = np.clip(ix2 - ix1, 0, None)`.

</details>

<details><summary>Hint 3</summary>

`union = areaA[:, None] + areaB[None, :] - inter`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | IoU = intersection / (areaA + areaB − intersection). |
| `test_touching` | Clip negative intersection widths/heights to 0. |
| `test_contained` | Use max of the top-left corners and min of the bottom-right corners. |
| `test_degenerate` | Reject boxes with x2 <= x1 or y2 <= y1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Broadcasting A against B produces all pairwise intersection rectangles at once; clipping makes
non-overlapping pairs contribute zero. Union follows from inclusion–exclusion.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

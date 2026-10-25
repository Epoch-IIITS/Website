# CV-14 · 2D Max Pooling

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** CV-10 2D Filtering (Blur)

Read the lesson first: [article.md](article.md)

## Task

Write `pool2d(x, size=2, stride=None, mode="max")` for a 2-D array: `stride` defaults to `size`;
`mode` in {"max", "avg"}. Output shape `((H-size)//stride + 1, (W-size)//stride + 1)`. Raise
`ValueError` for invalid size/stride/mode or if the window is larger than the input.

**Example**
```python
x = np.arange(1, 17).reshape(4, 4)
pool2d(x)                 # [[ 6,  8], [14, 16]]
pool2d(x, mode="avg")     # [[ 3.5,  5.5], [11.5, 13.5]]
pool2d(x, size=3, stride=1)   # [[11, 12], [15, 16]]
```

## Hints

<details><summary>Hint 1</summary>

`Ho = (H - size) // stride + 1` (same for W).

</details>

<details><summary>Hint 2</summary>

General case: `sliding_window_view(x, (size, size))[::stride, ::stride]` has shape `(Ho, Wo, size, size)`.

</details>

<details><summary>Hint 3</summary>

Reduce with `.max(axis=(2, 3))` or `.mean(axis=(2, 3))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_max` | Non-overlapping 2×2 windows: stride defaults to size. |
| `test_crop` | Drop rows/columns that don't fill a whole window. |
| `test_overlap` | With stride < size, windows overlap; take every stride-th window. |
| `test_errors` | Reject windows larger than the input and unknown modes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`sliding_window_view` exposes every window; taking every `stride`-th window along both axes gives
exactly the pooled grid, whose shape matches the output-size formula. Reducing over the last two
axes computes the max or mean of each window.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

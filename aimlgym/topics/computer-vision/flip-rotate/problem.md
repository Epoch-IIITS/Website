# CV-05 · Flip and Rotate

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** CV-01 Images as Arrays

Read the lesson first: [article.md](article.md)

## Task

Implement (return arrays; `(H, W)` or `(H, W, C)` input):
* `flip_horizontal(img)`, `flip_vertical(img)`.
* `rotate90_cw(img, k=1)` → rotate clockwise by 90°·k (any integer k, negative = counter-clockwise),
  **without** `np.rot90`.

**Example**
```python
a = np.array([[1, 2, 3], [4, 5, 6]])
rotate90_cw(a)     # [[4, 1], [5, 2], [6, 3]]
flip_horizontal(a) # [[3, 2, 1], [6, 5, 4]]
```

## Hints

<details><summary>Hint 1</summary>

Slicing: `img[:, ::-1]` and `img[::-1]`.

</details>

<details><summary>Hint 2</summary>

One clockwise step: `np.swapaxes(img, 0, 1)[:, ::-1]`.

</details>

<details><summary>Hint 3</summary>

Use `k % 4` repetitions.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_cw` | Clockwise = swap spatial axes, then flip horizontally. |
| `test_matches_rot90_negative` | np.rot90 is counter-clockwise; use k % 4 steps of your own rotation. |
| `test_color` | Only swap axes 0 and 1 so channels stay last (don't use .T on 3-D arrays). |
| `test_flips` | Horizontal flip reverses columns: img[:, ::-1]. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Negative-step slices reverse an axis. Swapping the two spatial axes and then reversing columns
maps pixel (r, c) to (c, H−1−r), a clockwise quarter turn; channels stay last because only axes
0 and 1 are swapped.

## References

- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

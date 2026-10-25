# CV-07 · Binary Thresholding

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** CV-02 RGB to Grayscale

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `threshold(gray, t, invert=False)` → boolean mask (`gray > t`, or `gray <= t` if inverted).
* `foreground_fraction(mask)` → float fraction of True pixels (raise `ValueError` for empty).
* `apply_mask(img, mask)` → copy of `img` (gray or colour) with pixels outside the mask set to 0;
  raise `ValueError` if spatial shapes differ.

**Example**
```python
g = np.array([[10, 200], [128, 127]])
threshold(g, 127)            # [[False, True], [True, False]]
foreground_fraction(threshold(g, 127))   # 0.5
```

## Hints

<details><summary>Hint 1</summary>

`m = np.asarray(gray) > t`; return `~m` if invert.

</details>

<details><summary>Hint 2</summary>

`float(np.mean(mask))`.

</details>

<details><summary>Hint 3</summary>

For colour: `mask[..., None]` broadcasts over channels; use `np.where`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_threshold` | Use strict > t (127 is not foreground at t = 127). |
| `test_apply_color` | Broadcast the mask over channels with mask[..., None]. |
| `test_no_mutation` | Return a new array (np.where) instead of assigning into img. |
| `test_shape_mismatch` | Compare img.shape[:2] with mask.shape. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A comparison produces the mask; inversion is logical NOT. The mean of a boolean mask is the
foreground fraction. Masking uses `np.where`, adding a channel axis for colour images so the mask
broadcasts, and preserves the input dtype.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)

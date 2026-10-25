# CV-01 · Images as Arrays

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** DL-24 1-D Convolution with nn.Conv1d

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `image_info(img)` → dict with `height`, `width`, `channels` (1 for a 2-D image) and `dtype`
   (as a string, e.g. `"uint8"`).
2. `adjust(img, brightness=0, contrast=1.0)` → `uint8` image computed in float as
   `(img - 128) * contrast + 128 + brightness`, rounded with `np.rint`, then clipped to [0, 255].
3. `to_float(img)` → `float64` array in [0, 1] (divide by 255).
4. `to_uint8(x)` → inverse of `to_float`: multiply by 255, round, clip, convert.
5. `channels_first(img)` (H, W, C) → (C, H, W) and `channels_last(x)` (C, H, W) → (H, W, C);
   raise `ValueError` if the input is not 3-D.

## Hints

<details><summary>Hint 1</summary>

`channels = img.shape[2] if img.ndim == 3 else 1`; `str(img.dtype)` gives the dtype name.

</details>

<details><summary>Hint 2</summary>

`out = (img.astype(float) - 128) * contrast + 128 + brightness`, then `np.clip(np.rint(out), 0, 255).astype(np.uint8)`.

</details>

<details><summary>Hint 3</summary>

`np.transpose(img, (2, 0, 1))` and `np.transpose(x, (1, 2, 0))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_brightness_no_wraparound` | Convert to float before adding, then clip to [0, 255]. |
| `test_contrast` | Scale around 128: `(img - 128) * contrast + 128`, round with np.rint, clip. |
| `test_float_round_trip` | Divide by 255 for floats; multiply by 255 and round to go back. |
| `test_to_uint8_rounds_and_clips` | Round with `np.rint` before converting; don't truncate. |
| `test_channels` | Use `np.transpose` with axes (2, 0, 1) and (1, 2, 0). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All arithmetic happens in float so nothing wraps around; one helper rounds, clips and converts
back to `uint8`. Normalisation is a division by 255 and its inverse a multiplication.
Transposing the axes moves the channel dimension without copying pixel values.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)

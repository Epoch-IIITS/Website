# CV-10 · 2D Filtering (Blur)

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** CV-02 RGB to Grayscale, DL-24 1-D Convolution with nn.Conv1d

Read the lesson first: [article.md](article.md)

## Task

Implement for 2-D float images:
* `filter2d(img, kernel, mode="zero")` → same-size output; `mode` in {"zero", "edge"}. Kernel
  dimensions must be odd, else `ValueError`. Vectorise over the kernel (looping over kernel
  entries is fine; avoid looping over every pixel).
* `box_kernel(k)` → `(k, k)` with all entries `1/k²` (odd k ≥ 1).
* `gaussian_kernel(k, sigma)` → normalised Gaussian (odd k, sigma > 0).

**Example**
```python
filter2d(np.ones((3, 3)), box_kernel(3))           # [[4/9, 6/9, 4/9], [6/9, 1, 6/9], [4/9, 6/9, 4/9]]
filter2d(np.ones((3, 3)), box_kernel(3), "edge")   # all ones
```

## Hints

<details><summary>Hint 1</summary>

`P = np.pad(img, ((rh, rh), (rw, rw)), mode='constant' or 'edge')`.

</details>

<details><summary>Hint 2</summary>

Loop over kernel offsets: `out += K[u, v] * P[u:u+H, v:v+W]`.

</details>

<details><summary>Hint 3</summary>

Gaussian: `ax = np.arange(k) - k // 2`; `g = np.exp(-(ax[:, None]**2 + ax[None, :]**2) / (2*sigma**2))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_box_zero` | Zero padding: border outputs average in zeros. |
| `test_no_flip` | Cross-correlation: an impulse reproduces the kernel flipped — don't flip it yourself. |
| `test_against_naive` | Pad by kernel_size // 2 on each side; out[i, j] uses P[i:i+kh, j:j+kw]. |
| `test_gaussian` | Normalise the Gaussian so it sums to 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Padding by the kernel radius keeps the output size equal to the input. Instead of looping over
pixels, the code loops over the (few) kernel entries and adds a shifted copy of the padded image
weighted by that entry — a vectorised cross-correlation.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)

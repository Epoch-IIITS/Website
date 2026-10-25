# 2-D Filtering

## Learning outcomes

After this lesson you can:

- Implement 2-D cross-correlation with 'same' output size
- Choose border handling (zero vs edge)
- Build box and Gaussian kernels

## Intuition
Blurring replaces each pixel by an average of its neighbourhood. Slide a small grid of weights
(kernel) over the image; at each position, multiply and add.

## Precise explanation
For an odd-sized kernel `(kh, kw)` with radius $r_h = kh//2$, $r_w = kw//2$:
$$\text{out}[i, j] = \sum_{u,v} \text{pad}(img)[i+u,\ j+v]\cdot K[u, v],$$
after padding by $(r_h, r_w)$ so the output has the **same** size as the input. This is
cross-correlation (no kernel flip), as in CNN layers (DL-25) and OpenCV's `filter2D`.
Border modes: **zero** padding (`np.pad(..., mode="constant")`) darkens edges; **edge** padding
(`mode="edge"`) repeats the border pixel.
* Box kernel: all entries $1/k^2$.
* Gaussian kernel: $G[u,v] \propto \exp(-(x^2+y^2)/(2\sigma^2))$ with $x, y \in \{-r..r\}$,
  normalised to sum to 1 (so overall brightness is preserved).

## Worked example
3×3 box blur on a 3×3 image of ones with zero padding: centre 1.0, edges 6/9, corners 4/9.
With edge padding every output is 1.0.

## Common mistakes
* Even-sized kernels (no centre) — reject them here.
* Using `np.convolve`/flipping the kernel.
* Not normalising blur kernels (image gets brighter).

## Why this matters
Every convolutional layer is this operation with learned kernels; smoothing is also a standard
pre-step before edge detection (CV-12).

## Library implementation

`scipy.ndimage.correlate(img, kernel, mode="constant", cval=0.0)` computes the same zero-padded
filter, and `mode="nearest"` matches edge padding. OpenCV's `cv2.filter2D` is the equivalent in
OpenCV. The comparison runs when SciPy is installed.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)

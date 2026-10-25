# Sobel Edge Detection

## Learning outcomes

After this lesson you can:

- Estimate image gradients with Sobel kernels
- Combine gradients into magnitude and direction
- Threshold edges

## Intuition
An edge is where brightness changes quickly. The Sobel operator estimates the horizontal and
vertical brightness change at every pixel, smoothing slightly to resist noise.

## Precise explanation
Sobel kernels (applied as cross-correlation, CV-10):
$$K_x = \begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix},\qquad K_y = K_x^\top.$$
$G_x$ responds to vertical edges (left→right change), $G_y$ to horizontal edges (top→bottom).
Magnitude $\sqrt{G_x^2 + G_y^2}$; direction $\operatorname{atan2}(G_y, G_x)$.
We compute **valid** outputs only (no padding), so the result is `(H−2, W−2)` and border artefacts
are avoided.

## Worked example
Image with left half 0 and right half 10 (vertical edge): $G_x$ = 40 along the edge, $G_y$ = 0;
magnitude 40.

## Common mistakes
* Swapping $K_x$ and $K_y$.
* Using `uint8` (negative gradients wrap around).
* Expecting thin edges — Sobel gives thick responses; non-maximum suppression (Canny) thins them.

## Why this matters
Edge maps were the foundation of classical vision; CNNs' first layers learn Sobel-like filters.

## Library implementation

`scipy.ndimage.sobel(img, axis=1)` and `axis=0` compute the horizontal and vertical Sobel
derivatives (with border handling); on interior pixels they equal your valid-region `gx` and `gy`.
`np.hypot(gx, gy)` gives the magnitude in both cases.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)

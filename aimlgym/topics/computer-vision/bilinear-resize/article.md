# Bilinear Resizing

## Learning outcomes

After this lesson you can:

- Map output pixels to input coordinates with half-pixel centres
- Interpolate bilinearly between four neighbours
- Vectorise with fancy indexing

## Intuition
To enlarge an image, each new pixel must be invented from nearby old pixels. Nearest-neighbour copies
the closest pixel (blocky). Bilinear blends the four surrounding pixels, weighted by distance
(smooth).

## Precise explanation
**Coordinate mapping (half-pixel centres, the convention OpenCV's `INTER_LINEAR` uses):** for output
row $i$ with scale $s_y = H_\text{in}/H_\text{out}$:
$$y = (i + 0.5)\,s_y - 0.5,$$
clamped to $[0, H_\text{in}-1]$ (same for columns). Let $y_0 = \lfloor y\rfloor$,
$y_1 = \min(y_0+1, H_\text{in}-1)$, $w_y = y - y_0$ (and similarly $x_0, x_1, w_x$). Then
$$\text{out} = (1-w_y)(1-w_x)\,I[y_0,x_0] + (1-w_y)w_x\,I[y_0,x_1] + w_y(1-w_x)\,I[y_1,x_0] + w_y w_x\,I[y_1,x_1].$$
Vectorise by computing row and column coordinate vectors once and using fancy indexing with
`np.ix_`-style broadcasting.

## Worked example
2×2 image [[0, 10], [20, 30]] → 4×4: output (0,0) maps to y = x = −0.25 → clamped 0 → 0;
output (1,1) maps to 0.25, 0.25 → 0.75·0.75·0 + 0.75·0.25·10 + 0.25·0.75·20 + 0.25·0.25·30 = 7.5.

## Common mistakes
* Using $y = i\cdot s_y$ (shifts the image by half a pixel).
* Forgetting to clamp, indexing out of bounds.
* Integer division in scale computation.

## Why this matters
Resizing to a fixed input size is the first step of almost every vision model; inconsistent
resizing between training and deployment is a known source of accuracy loss.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)

# Intersection over Union (IoU)

## Learning outcomes

After this lesson you can:

- Compute box areas and intersections
- Vectorise pairwise IoU with broadcasting
- Handle non-overlapping and degenerate boxes

## Intuition
How well does a predicted box match the true box? Divide the overlapping area by the total area
covered by either box. 1 = perfect match, 0 = no overlap.

## Precise explanation
Boxes as `[x1, y1, x2, y2]` with $x2 > x1$, $y2 > y1$ (continuous coordinates):
* area $= (x2-x1)(y2-y1)$;
* intersection corners: $\max(x1)$, $\max(y1)$, $\min(x2)$, $\min(y2)$; width/height clipped at 0;
* $\text{IoU} = \frac{|A\cap B|}{|A| + |B| - |A\cap B|}$.
Pairwise for $A$ `(m, 4)`, $B$ `(n, 4)`: broadcast `A[:, None, :]` against `B[None, :, :]` to get
`(m, n)` matrices. Detection benchmarks count a prediction as correct if IoU ≥ 0.5 (or several
thresholds).

## Worked example
A = [0, 0, 2, 2], B = [1, 1, 3, 3]: intersection 1×1 = 1; union 4 + 4 − 1 = 7 → IoU 1/7 ≈ 0.143.

## Common mistakes
* Forgetting to clip negative widths (non-overlapping boxes give negative "intersection").
* Mixing `[x, y, w, h]` and `[x1, y1, x2, y2]` formats.
* +1 pixel conventions from integer-pixel datasets (we use continuous coordinates).

## Why this matters
IoU drives detection evaluation (mAP), anchor matching during training and non-maximum suppression
(CV-24).

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

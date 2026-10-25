# XA-09 · Occlusion Saliency Map

**Topic:** Explainable AI · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** CV-13 Pooling with nn.MaxPool2d and nn.AvgPool2d, XA-04 Individual Conditional Expectation

Read the lesson first: [article.md](article.md)

## Task

Write `occlusion_map(score_fn, img, patch=2, baseline=0.0)` for a 2-D image returning a float array
of shape `(ceil(H/patch), ceil(W/patch))` as described. `img` must not change. Raise `ValueError`
if `patch < 1`.

**Example**
```python
score = lambda im: float(im[:2, :2].sum())
occlusion_map(score, np.ones((4, 4)), patch=2)   # [[4., 0.], [0., 0.]]
```

## Hints

<details><summary>Hint 1</summary>

`Hp = -(-H // patch)` is ceil division.

</details>

<details><summary>Hint 2</summary>

For each (pi, pj): `occ = img.copy(); occ[pi*patch:(pi+1)*patch, pj*patch:(pj+1)*patch] = baseline`.

</details>

<details><summary>Hint 3</summary>

`sal[pi, pj] = base - score_fn(occ)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_edge_patches` | Use ceil division for the map shape; edge patches are smaller. |
| `test_linear_model` | Saliency = original score − occluded score. |
| `test_no_mutation` | Occlude a copy of the image for every patch. |
| `test_baseline_value` | Fill occluded pixels with the baseline value. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each patch is occluded on a fresh copy; slicing past the edge automatically gives smaller edge
patches. The saliency is the score drop relative to the unoccluded image.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)

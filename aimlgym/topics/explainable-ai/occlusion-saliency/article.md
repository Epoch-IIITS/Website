# Occlusion Saliency

## Learning outcomes

After this lesson you can:

- Occlude image patches with a baseline value
- Measure the drop in class score per patch
- Build a saliency heat-map at patch resolution

## Intuition
Cover part of an image with a grey square. If the classifier's confidence in "dog" drops sharply, that
region mattered. Slide the square over the whole image to build a heat-map of importance.

## Precise explanation
For a scoring function `score_fn(img) -> float` (e.g. the logit of the predicted class):
1. Reference score $s = \text{score}(I)$.
2. For each non-overlapping patch (top-left corners on a grid with step `patch`; edge patches may be
   smaller), set its pixels to `baseline` and compute $s_{p}$.
3. Saliency of the patch = $s - s_p$ (positive = the patch supported the score).
Output shape: `(ceil(H/patch), ceil(W/patch))`. This is a **perturbation** method: model-agnostic but
needs one forward pass per patch. The baseline (black, grey, blurred) changes the answer.

## Worked example
score = sum of the top-left 2×2 region of a 4×4 image of ones, patch 2: occluding the top-left patch
drops the score from 4 to 0 → saliency 4; other patches → 0.

## Common mistakes
* Occluding the original array in place (corrupts later patches).
* Forgetting partial patches at the right/bottom edges.
* Interpreting saliency as "what the model sees" — it measures sensitivity to this particular
  perturbation.

## Why this matters
Occlusion maps (and gradient saliency) are common sanity checks for vision models, e.g. revealing
models that rely on watermarks or backgrounds.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)

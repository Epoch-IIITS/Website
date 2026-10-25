# Explaining a Linear Prediction

## Learning outcomes

After this lesson you can:

- Attribute a linear prediction to features relative to a baseline
- Verify that contributions sum to prediction − baseline prediction
- Explain why the baseline choice matters

## Intuition
A linear model is a weighted sum, so its prediction splits naturally into one piece per feature.
But "feature 2 contributed +30" only makes sense *relative to something*: compared with an average
customer, a zero input, or last month's value.

## Precise explanation
For $f(x) = w\cdot x + b$ and a **baseline** (reference) input $x'$ (often the training mean):
$$\phi_j = w_j\,(x_j - x'_j),\qquad \sum_j \phi_j = f(x) - f(x').$$
The second property — contributions add up exactly to the difference from the baseline prediction —
is called **efficiency** (or local accuracy). Using $\phi_j = w_jx_j$ (baseline 0) is a special case
and can be misleading when 0 is not a meaningful input (age 0, temperature 0 K).
Interpretation also depends on feature scale: standardised features make $w_j$ comparable.

## Worked example
w = [2, −1], b = 5, x = [3, 4], baseline = mean [1, 1]: φ = [4, −3]; f(x) = 7, f(x′) = 6,
sum φ = 1 = 7 − 6 ✓.

## Common mistakes
* Reporting $w_j$ alone as "importance" for one prediction (ignores the input value).
* Forgetting the baseline: contributions then do not add up to anything interpretable.
* Comparing weights of unscaled features.

## Why this matters
This is the simplest *exact* attribution; Shapley values (XA-11) reduce to exactly this formula for
linear models with independent features.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)

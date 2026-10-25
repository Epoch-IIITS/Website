# Global Surrogate Models

## Learning outcomes

After this lesson you can:

- Fit an interpretable model to a black box's predictions
- Measure fidelity with R² against the black box
- Recognise when a surrogate explanation cannot be trusted

## Intuition
Train a simple, readable model (linear or a small tree) to *imitate the black box*. If the imitation
is faithful, its structure explains the black box; if not, the explanation is fiction.

## Precise explanation
1. Query the black box: $\hat y = f(X)$ on representative data.
2. Fit the surrogate $g$ to $(X, \hat y)$ — note: the **black-box predictions**, not the true labels.
3. **Fidelity:** $R^2(\hat y, g(X))$ — how much of the black box's behaviour the surrogate captures.
Only interpret a surrogate with high fidelity (and check fidelity on held-out data). Fidelity says
nothing about whether the black box is *correct* — only whether the surrogate copies it.

Linear surrogate: least squares on $[1, X]$ (NP-12).

## Worked example
Black box $f(x) = 2x_0 - x_1 + 3$: linear surrogate recovers intercept 3, weights [2, −1], fidelity 1.
Black box $f(x) = x_0^2$ on symmetric data: best line is flat, fidelity ≈ 0 → do not trust it.

## Common mistakes
* Fitting the surrogate to true labels (that just trains another model).
* Reporting the surrogate's accuracy on the task as "fidelity".
* Interpreting a low-fidelity surrogate.

## Why this matters
Surrogates are a practical way to summarise complex models, and the fidelity check is a habit every
explanation method deserves.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)

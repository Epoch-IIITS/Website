# Presenting Attributions

## Learning outcomes

After this lesson you can:

- Rank features by absolute attribution
- Report direction (sign) and share of total effect
- Produce a deterministic, human-readable explanation

## Intuition
An explanation with 300 numbers explains nothing. Show the few features that moved the prediction
most, with their direction ("raised"/"lowered") and how much of the total effect they account for.

## Precise explanation
Given attributions $\phi_j$ (e.g. from XA-01, XA-11):
* rank by $|\phi_j|$ descending (ties → feature name ascending, for determinism);
* direction: "+" if $\phi_j > 0$, "−" if $\phi_j < 0$, "0" otherwise;
* share $= |\phi_j| / \sum_i |\phi_i|$ (0 if all attributions are 0).
Sorting by absolute value matters: a large negative effect is as important as a large positive one.

## Worked example
names [age, income, debt], φ = [0.5, −2.0, 1.5] → ranking income (−, 0.5), debt (+, 0.375),
age (+, 0.125).

## Common mistakes
* Sorting by signed value (hides strong negative effects).
* Shares computed from signed sums (can divide by ~0).
* Non-deterministic order for ties.

## Why this matters
Explanations are for people; clear, stable presentation is part of building trustworthy systems
(Molnar's book discusses human-friendly explanations).

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)

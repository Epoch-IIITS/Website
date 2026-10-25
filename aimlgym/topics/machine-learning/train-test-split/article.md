# Train/Test Splits

## Learning outcomes

After this lesson you can:

- Split data into disjoint train and test sets
- Keep X and y aligned when shuffling
- Implement a stratified split

## Intuition
A model is useful only if it works on data it hasn't seen. Hold some data back — the **test
set** — and never use it for training or tuning; it estimates performance on new data.

## Precise explanation
* Shuffle indices once (seeded), then take the first `n_test` as test and the rest as train.
  Index X and y with the **same** index arrays so features and labels stay paired.
* `n_test = round(n * test_size)` (here, and at least 1 and at most n − 1).
* **Stratified split:** keep class proportions similar in train and test by splitting each class
  separately and combining. Important for imbalanced classes — a random split of 95/5 data might
  put no minority examples in the test set.
* Typical sizes: 70–80 % train, 20–30 % test; a separate validation set (or cross-validation,
  ML-17) is used for tuning.

## Worked example
n = 8, test_size = 0.25 → n_test = 2. With a permutation [5, 2, 7, 0, 1, 3, 6, 4], test rows
are 5, 2 and train rows the other six.

## Common mistakes
* Shuffling X and y separately (pairs broken).
* Splitting *after* preprocessing with statistics from all data (leakage; ML-08).
* Unseeded splits, making results irreproducible.

## Why this matters
Every evaluation in the remaining topics depends on an honest, reproducible split.

## Library implementation

scikit-learn's `train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)` does the same
job with its own random generator, so the chosen rows differ from yours; it also rounds the test
size **up** (`ceil`) where this exercise rounds to nearest. What must agree is the contract: the
two parts are disjoint, together contain every row, and stratification preserves class
proportions. The test checks that contract on scikit-learn's output and yours when it is
installed.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)

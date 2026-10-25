# Polynomial Features and Overfitting

## Learning outcomes

After this lesson you can:

- Turn one feature into polynomial features [1, x, x², …]
- Fit polynomial models with least squares
- Show that training error falls with degree while test error eventually rises
- Choose model complexity using held-out data

## Intuition
A straight line cannot follow a curve: it **underfits**. A polynomial of very high degree can pass
through every training point, wiggling wildly in between: it **overfits** — it memorises noise
and predicts new points badly. The right complexity sits in between, and the only honest way to
find it is to measure error on data the model did not train on.

## Precise explanation
* **Polynomial features**: for a single input $x$, build columns $[1, x, x^2, \dots, x^d]$. A
  *linear* model on these columns is a degree-$d$ polynomial in $x$ — so least squares still
  applies.
* **Fitting**: solve $\min_w \lVert Xw - y\rVert^2$ with `np.linalg.lstsq(X, y, rcond=None)`,
  which handles the case where columns are nearly dependent.
* **Training error never increases with degree**: each larger model contains the smaller one (set
  the extra coefficients to 0), so its best training fit is at least as good.
* **Test error** first falls (less underfitting), then rises (overfitting). Pick the degree with the
  lowest error on held-out data; ML-17 makes that choice more reliable.
* **Bias–variance**: simple models are biased (systematically wrong); complex models have high
  variance (very sensitive to which training points you happened to get).

## Worked example
Ten training points from $y = 1 + 2x - 3x^2$ plus small noise: degree 1 leaves a large training
error; degree 2 fits almost perfectly on both sets; degree 9 interpolates all ten training points
(training error ≈ 0) but its test error is far larger than degree 2's.

## Common mistakes
* Selecting the degree by training error — it always picks the largest degree.
* Using the test set to choose the degree and then reporting that same test error as final.
* Forgetting the constant column, which forces the curve through the origin.

## Why this matters
Every model has a complexity knob (tree depth, number of neighbours, network size, training
epochs). Recognising over- and underfitting from train/test errors is a core ML skill.

## Library implementation

NumPy's `np.polyfit(x, y, degree)` fits the same polynomial (it returns the **highest** power
first), and scikit-learn builds it as a pipeline:
`make_pipeline(PolynomialFeatures(degree), LinearRegression())`. `PolynomialFeatures` is what
your `poly_features` does; `LinearRegression` solves the least-squares problem. Their scikit-learn
example "Underfitting vs. Overfitting" draws the same curves you computed. The tests compare
with `np.polyfit`, and with scikit-learn when it is installed.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Underfitting vs. Overfitting (scikit-learn example)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html) — scikit-learn developers (`S090`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

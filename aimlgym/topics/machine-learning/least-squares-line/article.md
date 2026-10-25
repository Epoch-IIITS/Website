# Fitting a Line by Least Squares

## Learning outcomes

After this lesson you can:

- Derive the closed-form slope and intercept
- Predict with a fitted line
- Relate slope to covariance/variance

## Intuition
Among all straight lines, pick the one that makes the squared vertical gaps to the points as
small as possible. Squaring treats over- and under-predictions alike and gives a closed-form
answer.

## Precise explanation
Minimise $L(a, b) = \sum (y_i - (a + b x_i))^2$. Setting both partial derivatives to zero gives
$$b = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sum (x_i-\bar x)^2} = \frac{\operatorname{cov}(x,y)}{\operatorname{var}(x)},\qquad a = \bar y - b\bar x.$$
The fitted line always passes through $(\bar x, \bar y)$. If all $x$ are equal the slope is
undefined. In matrix form (many features) this is the normal equation
$w = (X^\top X)^{-1} X^\top y$ (NP-12 used `lstsq`; ML-20 adds regularisation).

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="170" viewBox="0 0 260 170" role="img" aria-label="Scatter of five points with a fitted line and vertical residual segments">
<title>Least-squares residuals</title>
<line x1="20" y1="150" x2="250" y2="150" stroke="#999"/><line x1="20" y1="150" x2="20" y2="10" stroke="#999"/>
<line x1="30" y1="140" x2="240" y2="30" stroke="#1f77b4" stroke-width="2"/>
<circle cx="50" cy="118" r="4"/><line x1="50" y1="118" x2="50" y2="129.5" stroke="#d62728"/>
<circle cx="90" cy="118" r="4"/><line x1="90" y1="118" x2="90" y2="108.6" stroke="#d62728"/>
<circle cx="140" cy="70" r="4"/><line x1="140" y1="70" x2="140" y2="82.4" stroke="#d62728"/>
<circle cx="190" cy="66" r="4"/><line x1="190" y1="66" x2="190" y2="56.2" stroke="#d62728"/>
<circle cx="225" cy="30" r="4"/><line x1="225" y1="30" x2="225" y2="37.9" stroke="#d62728"/>
</svg>

*Figure (original): the blue line minimises the sum of squared red residuals.*

## Worked example
x = [1, 2, 3, 4], y = [2, 4, 5, 8] → b = 9.5/5 = 1.9, a = 4.75 − 1.9·2.5 = 0. Prediction at
x = 5: 9.5.

## Common mistakes
* Minimising perpendicular distances (that is a different method).
* Forgetting the intercept.
* Extrapolating far beyond the training x-range.

## Why this matters
Linear regression is the baseline model for every regression task and the building block of
GLMs, neural network output layers and many explanations (XA-01).

## Library implementation

`np.polyfit(x, y, 1)` and scikit-learn's `LinearRegression().fit(x.reshape(-1, 1), y)` fit the
same line; `LinearRegression.score` is the same $R^2$. The NumPy comparison always runs; the
scikit-learn one runs when it is installed.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)

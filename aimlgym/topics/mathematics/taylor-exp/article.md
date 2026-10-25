# Approximating Functions with Taylor Series

## Learning outcomes

After this lesson you can:

- Evaluate a truncated Taylor series
- Compute terms recursively to avoid factorials
- Stop based on a tolerance

## Intuition
Near a point, smooth functions look like polynomials. A Taylor series builds that polynomial
term by term; adding more terms extends the region where it matches.

## Precise explanation
The Taylor series of $e^x$ around 0:
$$e^x = \sum_{k=0}^{\infty} \frac{x^k}{k!} = 1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots$$
Truncating after $n$ terms gives an approximation. Compute terms **recursively** rather than
with powers and factorials:
$$t_0 = 1,\qquad t_k = t_{k-1}\cdot\frac{x}{k}.$$
This avoids overflow in $k!$ and is cheaper.

**Stopping rule:** keep adding terms until the next term's magnitude is below a tolerance.

For large negative $x$, alternating terms cancel badly (loss of precision). A standard fix is
$e^{x} = 1/e^{-x}$ for $x<0$ — you can try it as an extension.

## Worked example
$e^1$ with 5 terms: $1 + 1 + 0.5 + 0.1\overline{6} + 0.041\overline{6} = 2.708\overline{3}$;
true value 2.71828…

## Common mistakes
* Starting the sum at $k=1$ and missing the constant term 1.
* Off-by-one in "number of terms" (5 terms means $k = 0..4$).
* Using `math.factorial` and `x**k` for large k → `OverflowError` or slow code.

## Why this matters
Linear (first-order) Taylor approximations justify gradient descent, and second-order ones
justify Newton's method. Softmax and sigmoid are built on $e^x$.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)

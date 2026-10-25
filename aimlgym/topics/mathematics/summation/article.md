# Summation and Product Notation

## Learning outcomes

After this lesson you can:

- Read Σ and Π notation and translate it into a loop
- Check a closed-form formula against a loop
- Explain why math.fsum is more accurate than repeated +

## Intuition
Mathematics writes "add up these terms" with a big Greek S, **Σ** (sigma), and "multiply
them" with a big P, **Π** (pi). Almost every formula in ML — means, losses, dot products,
likelihoods — is a Σ or a Π, and each one is just a loop.

## Precise explanation
$$\sum_{i=a}^{b} f(i) = f(a) + f(a+1) + \dots + f(b), \qquad
  \prod_{i=a}^{b} f(i) = f(a)\,f(a+1)\cdots f(b).$$
* The index $i$ runs over every integer from $a$ to $b$ **inclusive**. If $b < a$ the sum is
  empty and equals 0; the empty product equals 1.
* In Python: `total = 0; for i in range(a, b + 1): total += f(i)`.
* The mean of $x_1, \dots, x_n$ is $\bar x = \frac{1}{n}\sum_{i=1}^{n} x_i$. Code indexes from 0,
  maths usually from 1: $x_1$ is `xs[0]`.
* Closed forms replace a loop with a formula, e.g. $\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$.
  Checking a formula against a loop is a reliable way to catch algebra mistakes.

**Floating-point sums.** Floats are stored in binary, so `0.1` is slightly off and errors add
up: `0.1 + 0.1 + ... (10 times)` is `0.9999999999999999`. `math.fsum` tracks the lost low-order
digits and returns the correctly rounded `1.0`.

## Worked example
$\sum_{i=1}^{4} (2i + 1) = 3 + 5 + 7 + 9 = 24$; $\prod_{i=1}^{4} i = 24 = 4!$.

## Common mistakes
* `range(a, b)` misses the last term $b$.
* Starting a product at 0 instead of 1.
* Using `//` in closed forms and losing the fraction before multiplying: compute
  `n * (n + 1) * (2 * n + 1) // 6`, not `n // 6 * ...`.

## Why this matters
Losses average a Σ over examples, likelihoods are a Π over observations (MA-02 turns them
into sums), and MA-04 is a Σ over coordinates.

## Library implementation

Python's built-ins already implement these loops:

```python
sum(f(i) for i in range(a, b + 1))   # Σ — the built-in sum
math.prod(f(i) for i in range(a, b + 1))  # Π
math.fsum(xs)                        # Σ with correctly rounded floating-point result
statistics.fmean(xs)                 # mean, using an accurate float sum
```
`sum` and `math.prod` behave exactly like your loops (same rounding); `math.fsum` and
`statistics.fmean` are more accurate for floats. The test below checks your `mean` against
`statistics.fmean`.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)

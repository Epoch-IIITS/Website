# Gradient Checking

## Learning outcomes

After this lesson you can:

- Compare analytic and numerical gradients
- Use relative error with a safe denominator
- Locate the parameter with the worst mismatch

## Intuition
Backpropagation code can be subtly wrong and still "train" a bit. A gradient check compares your
analytic gradient with a slow but reliable numerical estimate (MA-14). If they disagree, there is
a bug.

## Precise explanation
For each coordinate $i$: $g^\text{num}_i = \frac{f(x + h e_i) - f(x - h e_i)}{2h}$.
Compare with the **relative error**
$$\text{rel}(a, b) = \frac{|a - b|}{\max(|a| + |b|,\ \text{tiny})},$$
which is scale-free; the `tiny` floor (1e−12 here) avoids 0/0 when both are zero. Rough guide for
float64 and smooth functions: < 1e−7 excellent, 1e−7…1e−4 suspicious, > 1e−4 almost certainly a
bug. Kinks (ReLU at 0) can cause false alarms.

## Worked example
f(x) = Σ x², grad 2x. At x = [1, −2], numerical [2, −4] → relative errors ~1e−11. A buggy grad
returning x gives rel = |2 − 1|/3 = 0.33.

## Common mistakes
* Using absolute error only (meaningless for very large or small gradients).
* h too small (round-off) or too large (truncation).
* Forgetting to restore x after perturbing.

## Why this matters
Every from-scratch implementation in this course was tested this way; it is the standard sanity
check before training any custom layer.

## References

- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

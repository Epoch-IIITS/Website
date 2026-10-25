# Integrated Gradients

## Learning outcomes

After this lesson you can:

- Integrate gradients along the straight path from a baseline
- Approximate the integral with a midpoint Riemann sum
- Check the completeness axiom

## Intuition
A plain gradient tells you the local slope, which can be zero for a saturated neuron even when the
feature mattered. Integrated gradients (IG) accumulate gradients along the whole path from a
baseline (e.g. a black image) to the input, so nothing that mattered along the way is missed.

## Precise explanation (Sundararajan et al., 2017)
$$\text{IG}_j(x) = (x_j - x'_j)\int_0^1 \frac{\partial f}{\partial x_j}\big(x' + \alpha(x - x')\big)\,d\alpha.$$
**Completeness:** $\sum_j \text{IG}_j = f(x) - f(x')$ (by the fundamental theorem of calculus along
the path). Approximate the integral with a **midpoint Riemann sum** over m steps:
$\alpha_k = (k + 0.5)/m$, $k = 0..m-1$, average the gradients and multiply by $(x - x')$. Error
shrinks as m grows (compare MA-12). For linear models IG equals $w_j(x_j - x'_j)$ — again matching
XA-01/XA-11.

## Worked example
f(x) = x₀²·x₁, x = (1, 2), baseline 0: ∂f/∂x₀ = 2x₀x₁, ∂f/∂x₁ = x₀². On the path (α, 2α):
∫ 4α² dα = 4/3 → IG₀ = 4/3; ∫ α² dα = 1/3 → IG₁ = 2/3; sum = 2 = f(x) ✓.

## Common mistakes
* Forgetting the (x − x′) factor.
* Endpoint Riemann sums with few steps (biased); use midpoints.
* Choosing a baseline that is not "neutral" for the task and misreading results.

## Why this matters
IG is a standard attribution method for neural networks (images, text) and satisfies axioms that
plain gradients violate.

## References

- [Axiomatic Attribution for Deep Networks](https://arxiv.org/abs/1703.01365) — Mukund Sundararajan, Ankur Taly, Qiqi Yan (`S027`)
- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)

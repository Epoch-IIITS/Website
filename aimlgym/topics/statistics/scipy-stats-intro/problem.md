# ST-14 · Introducing scipy.stats

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** numpy, scipy

**Builds on:** ST-09 The Normal Distribution

Read the lesson first: [article.md](article.md)

## Task

Write `distribution_facts(kind, params, x, q)` returning a dict of plain floats
`{"density": ..., "cdf": ..., "quantile": ..., "mean": ..., "std": ...}`.

* `kind="norm"`: `params = (mu, sigma)`; density is the pdf at `x`.
* `kind="binom"`: `params = (n, p)`; density is the pmf at `x`.
* `cdf` is evaluated at `x`, `quantile` is the ppf at `q`.
* Raise `ValueError` for an unknown kind, `sigma <= 0`, `n < 0`, `p` outside [0, 1], or `q` not
  strictly between 0 and 1.

Use `scipy.stats`.

**Examples**
```python
distribution_facts("norm", (170, 10), 180, 0.975)
# {'density': 0.0241..., 'cdf': 0.8413..., 'quantile': 189.59..., 'mean': 170.0, 'std': 10.0}
distribution_facts("binom", (10, 0.5), 5, 0.5)
# {'density': 0.24609375, 'cdf': 0.623046875, 'quantile': 5.0, 'mean': 5.0, 'std': 1.5811...}
```

## Hints

<details><summary>Hint 1</summary>

Validate first, then build `dist = stats.norm(loc=mu, scale=sigma)` or `stats.binom(n, p)`.

</details>

<details><summary>Hint 2</summary>

The density method is `dist.pdf(x)` for the normal and `dist.pmf(x)` for the binomial.

</details>

<details><summary>Hint 3</summary>

Convert every result with `float(...)` before putting it in the dict.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_normal_matches_formulas` | `scale` is the standard deviation σ, and ppf takes a probability q. |
| `test_binomial_matches_formulas` | Discrete distributions use `pmf`, not `pdf`. |
| `test_plain_floats` | Wrap SciPy results in `float(...)`. |
| `test_invalid_parameters` | Check the parameters yourself before calling SciPy; it returns nan instead of raising. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The frozen distribution holds the parameters, so every fact is one method call. Only the density
method differs between continuous (`pdf`) and discrete (`pmf`) families. Validation happens before
SciPy is called, because SciPy returns `nan` for invalid parameters instead of raising.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)

# FL-13 · Differentially Private Aggregation

**Topic:** Federated Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** FL-09 Clipping Client Updates, FL-02 Weighted Federated Averaging

Read the lesson first: [article.md](article.md)

## Task

Write `dp_mean(deltas, clip_norm, noise_multiplier, rng)` returning `(noisy_mean, clipped_mean, sigma)`:
clip each delta to `clip_norm` (FL-09 rule), average, and add `rng.normal(0, sigma, size=dim)` with
`sigma = noise_multiplier * clip_norm / m`. With `noise_multiplier == 0` do **not** draw noise
(return the clipped mean). Raise `ValueError` for empty deltas, `clip_norm <= 0` or
`noise_multiplier < 0`.

**Example**
```python
noisy, clean, sigma = dp_mean([np.array([3., 4.]), np.array([0.3, 0.4])], 1.0, 0.0, np.random.default_rng(0))
clean, sigma    # ([0.45, 0.6], 0.0)
```

## Hints

<details><summary>Hint 1</summary>

Clip: `d * min(1, C / ‖d‖)` (guard the zero vector).

</details>

<details><summary>Hint 2</summary>

`clipped_mean = np.mean(clipped, axis=0)`; `sigma = z * C / len(deltas)`.

</details>

<details><summary>Hint 3</summary>

Only call `rng.normal` when `sigma > 0`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_sigma` | sigma = noise_multiplier × clip_norm / m (number of participating clients). |
| `test_noise_recipe` | Add rng.normal(0, sigma, size=dim) to the clipped mean (one draw). |
| `test_sensitivity_bound` | Clip each update before averaging. |
| `test_no_noise` | With noise_multiplier = 0 return the clipped mean exactly. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Clipping bounds each client's contribution; averaging over m clients divides the sensitivity by m;
Gaussian noise with standard deviation z·C/m is then added to the mean. Skipping the draw when σ = 0
keeps the noiseless path exact and leaves the generator untouched.

## References

- [Learning Differentially Private Recurrent Language Models](https://arxiv.org/abs/1710.06963) — H. Brendan McMahan, Daniel Ramage, Kunal Talwar, Li Zhang (`S031`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)

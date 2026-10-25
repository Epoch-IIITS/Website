# Reproducible Randomness in NumPy

## Learning outcomes

After this lesson you can:

- Use np.random.default_rng with a seed
- Generate synthetic regression data
- Create reproducible shuffled train/test indices

## Intuition
Experiments must be repeatable: the same seed should give the same "random" data, so a teammate
can reproduce your numbers. NumPy's modern API puts all randomness in a `Generator` object.

## Precise explanation
* `rng = np.random.default_rng(seed)` creates an independent generator (PCG64 by default).
* `rng.uniform(lo, hi, size=n)`, `rng.normal(mu, sigma, size=n)`, `rng.permutation(n)`,
  `rng.integers(lo, hi, size=n)`.
* Passing a generator around (rather than calling the legacy global `np.random.seed`) keeps
  different parts of a program from disturbing each other's streams.
* Same seed → same numbers *in the same NumPy version*. NumPy reserves the right to change some
  algorithms between versions, so never hard-code random outputs in tests; test properties.

Synthetic linear data: $x \sim U(0, 1)$, $y = 2x + 1 + \varepsilon$, $\varepsilon \sim N(0, \sigma^2)$.

## Worked example
```python
rng = np.random.default_rng(0)
idx = rng.permutation(10)       # some ordering of 0..9
test, train = idx[:3], idx[3:]  # 30 % test
```

## Common mistakes
* Calling `default_rng(seed)` inside a loop — every iteration restarts the same stream.
* Using the global `np.random.rand` in library code.
* Overlapping train and test indices.

## Why this matters
Seeded data generation, shuffling and weight initialisation make every later ML, DL and FL
exercise deterministic.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)

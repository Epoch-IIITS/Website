# NP-10 · Seeded Random Generators

**Topic:** NumPy · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NP-09 Fancy Indexing and Gather, ST-10 Dice Simulation and the Law of Large Numbers

Read the lesson first: [article.md](article.md)

## Task

Implement using `np.random.default_rng(seed)` (one generator per call):
* `make_regression(n, seed, noise=0.1)` → `(x, y)` with `x = rng.uniform(0, 1, n)` drawn first,
  then `eps = rng.normal(0, noise, n)`, and `y = 2 * x + 1 + eps`. Raise `ValueError` if `n < 1`
  or `noise < 0`.
* `split_indices(n, test_frac, seed)` → `(train_idx, test_idx)` from `rng.permutation(n)`; the
  first `round(n * test_frac)` permuted indices are the test set. Raise `ValueError` unless
  `0 < test_frac < 1`.

**Examples**
```python
x, y = make_regression(5, seed=0)
x.shape, y.shape                # ((5,), (5,))
tr, te = split_indices(10, 0.3, seed=1)
len(tr), len(te)                # (7, 3)
```

## Hints

<details><summary>Hint 1</summary>

`rng = np.random.default_rng(seed)` once at the top of each function.

</details>

<details><summary>Hint 2</summary>

Draw x before the noise so the order of draws is as specified.

</details>

<details><summary>Hint 3</summary>

`perm = rng.permutation(n); k = round(n * test_frac); return perm[k:], perm[:k]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_draw_order` | Create one default_rng(seed); draw x = uniform first, then normal noise. |
| `test_reproducible` | Don't use the global np.random functions. |
| `test_split_disjoint_cover` | Use rng.permutation(n) and split it; the two parts must not overlap. |
| `test_noise_free` | y = 2x + 1 + noise exactly. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each function owns one seeded generator, so results depend only on the arguments. Draw order is
fixed (x then noise). The permutation guarantees train and test indices are disjoint and cover
0..n−1.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)

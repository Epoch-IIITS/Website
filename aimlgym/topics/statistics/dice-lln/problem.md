# ST-10 · Dice Simulation and the Law of Large Numbers

**Topic:** Statistics · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** ST-06 Probability by Counting Outcomes

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `roll(rng)` → one die face `int(rng.random() * 6) + 1`, using **only** `rng.random()`.
* `simulate_two_dice(n, seed)` → dict with keys
  * `"sums"`: list of `n` sums, each `roll(rng) + roll(rng)` (first die drawn first),
  * `"running_mean"`: list where element i is the mean of `sums[:i+1]`,
  * `"freq"`: dict mapping each sum 2..12 to its count (all 11 keys present),
  using `rng = random.Random(seed)`. Raise `ValueError` if `n < 1`.

**Examples**
```python
r = simulate_two_dice(5, seed=0)
len(r["sums"]) == 5 and all(2 <= s <= 12 for s in r["sums"])    # True
abs(simulate_two_dice(100000, seed=1)["running_mean"][-1] - 7) < 0.05   # True (LLN)
```

## Hints

<details><summary>Hint 1</summary>

`int(rng.random() * 6) + 1` maps [0,1) to 1..6.

</details>

<details><summary>Hint 2</summary>

Keep a running total; running_mean[i] = total / (i + 1).

</details>

<details><summary>Hint 3</summary>

Initialise `freq = {s: 0 for s in range(2, 13)}`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_exact_sequence` | Use random.Random(seed) and draw exactly two rng.random() calls per roll, first die first. |
| `test_roll_range` | Faces must be 1..6: int(u*6) + 1. |
| `test_freq_keys_and_total` | All sums 2..12 must be keys, even with count 0. |
| `test_running_mean` | running_mean[i] is the mean of the first i+1 sums. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A private generator seeded once makes the whole simulation reproducible. Each die face comes from
a single `rng.random()` call (the only output Python guarantees across versions). One loop records
the sum, updates the frequency table and the running mean.

## References

- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)

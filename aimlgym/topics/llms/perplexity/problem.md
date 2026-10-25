# LM-05 · Perplexity

**Topic:** Large Language Models · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** LM-02 Next-Token Probabilities (Add-k), DL-03 Cross-Entropy Loss

Read the lesson first: [article.md](article.md)

## Task

Implement for a non-empty list of probabilities in `[0, 1]`:
* `avg_nll(token_probs)` → mean of `-ln p` (`math.inf` if any p is 0).
* `perplexity(token_probs)` → `exp(avg_nll)` (`math.inf` if infinite).
Raise `ValueError` for empty input or values outside `[0, 1]`.

**Examples**
```python
perplexity([0.5, 0.25, 0.125])   # 4.0
perplexity([0.1] * 7)            # 10.0
perplexity([0.9, 0.0])           # inf
```

## Hints

<details><summary>Hint 1</summary>

Validate, then check `any(p == 0 for p in token_probs)`.

</details>

<details><summary>Hint 2</summary>

`-sum(math.log(p) for p in token_probs) / len(token_probs)`.

</details>

<details><summary>Hint 3</summary>

`math.exp(nll)` unless nll is inf.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Average −ln p over tokens, then exponentiate. |
| `test_not_mean_of_probs` | Perplexity is the inverse geometric mean, not 1 / arithmetic mean. |
| `test_zero` | Return math.inf if any probability is 0. |
| `test_invalid` | Validate empty input and range [0, 1]. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The average negative log-probability is the per-token cross-entropy; exponentiating gives
perplexity. Zero probabilities make the log undefined, so infinity is returned explicitly.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)

# ST-02 · Median and Mode

**Topic:** Statistics · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** ST-01 Mean and Variance (Population vs Sample)

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `median(data)` → float median; raise `ValueError` on empty input. Do not modify `data`.
* `modes(data)` → sorted list of all values with the highest frequency (`[]` for empty input).

**Examples**
```python
median([7, 1, 3, 3, 100])   # 3.0
median([4, 1, 2, 3])        # 2.5   — even length: mean of the two middle values
modes([1, 2, 2, 3, 3])      # [2, 3]
modes([5])                  # [5]
```

## Hints

<details><summary>Hint 1</summary>

Use `s = sorted(data)` (a new list) and `n = len(s)`.

</details>

<details><summary>Hint 2</summary>

Odd: `s[n // 2]`; even: average of `s[n // 2 - 1]` and `s[n // 2]`.

</details>

<details><summary>Hint 3</summary>

Count with a dict, find the max count, collect keys with that count, then sort.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_odd` | Sort before picking the middle element. |
| `test_even` | For even n, average the two middle values. |
| `test_modes_tie` | Return every value tied for the highest count, sorted. |
| `test_not_modified` | Use sorted(data), not data.sort(). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`sorted` returns a new list so the input is untouched; integer division picks the middle index
and the even case averages two values. `modes` counts frequencies with a dict and keeps every
value tied for the maximum count, sorted for a deterministic answer.

## References

- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)

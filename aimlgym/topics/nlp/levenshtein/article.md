# Edit Distance

## Learning outcomes

After this lesson you can:

- Fill a dynamic-programming table
- Compute minimum insert/delete/substitute edits
- Build a simple spelling suggester

## Intuition
How many single-character edits turn "kitten" into "sitting"? Substitute k→s, substitute e→i,
insert g: three. The smallest such number is the **Levenshtein distance**.

## Precise explanation
Let $D[i][j]$ be the distance between the first $i$ characters of $a$ and the first $j$ of $b$:
$$D[i][0] = i,\quad D[0][j] = j,$$
$$D[i][j] = \min\big(D[i-1][j] + 1,\ D[i][j-1] + 1,\ D[i-1][j-1] + [a_i \ne b_j]\big).$$
(deletion, insertion, substitution/match). The answer is $D[|a|][|b|]$. Time $O(|a||b|)$; only
two rows are needed for memory $O(|b|)$.

| | "" | s | i | t |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| k | 1 | 1 | 2 | 3 |
| i | 2 | 2 | 1 | 2 |
| t | 3 | 3 | 2 | 1 |

*Table: D for "kit" → "sit": distance 1.*

## Worked example
levenshtein("kitten", "sitting") = 3; levenshtein("", "abc") = 3.

## Common mistakes
* Forgetting the first row/column initialisation.
* Off-by-one between string index and table index (`a[i-1]`).
* Exponential recursion without memoisation.

## Why this matters
Edit distance powers spelling correction, fuzzy matching and evaluation metrics such as word error
rate in speech recognition.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)

# LM-06 · Byte-Pair Encoding Merges

**Topic:** Large Language Models · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** LM-01 Vocabularies and Token IDs

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `learn_bpe(word_counts, num_merges)` → list of merged pairs `(a, b)` in order. `word_counts` is a
  dict word → count. Each word starts as `tuple(word) + ("</w>",)`. Stop early if no pairs remain.
  Ties → smallest pair in Python tuple ordering.
* `apply_bpe(word, merges)` → list of symbols after applying merges in order.

**Example**
```python
m = learn_bpe({"low": 5, "lower": 2, "newest": 6, "widest": 3}, 3)
m                                 # [('e', 's'), ('es', 't'), ('est', '</w>')]
apply_bpe("lowest", m)            # ['l', 'o', 'w', 'est</w>']
```

## Hints

<details><summary>Hint 1</summary>

Keep `vocab = {tuple(w) + ('</w>',): c for w, c in word_counts.items()}`.

</details>

<details><summary>Hint 2</summary>

Pair counts: for each symbol tuple, add `c` to every `(s[i], s[i+1])`; best = `min(pairs, key=lambda p: (-pairs[p], p))`.

</details>

<details><summary>Hint 3</summary>

Write `_merge(symbols, pair)` scanning left to right, joining `a + b` when the pair matches.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_first_merges` | Weight each pair by its word's count and append '</w>' to every word. |
| `test_overlap` | Merge left to right without overlapping: 'aaa' → 'aa', 'a'. |
| `test_tie_lexicographic` | On ties choose the smallest pair: min(pairs, key=lambda p: (-count, p)). |
| `test_apply` | Apply merges in the order they were learned. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each round counts frequency-weighted adjacent pairs, picks the most frequent (smallest on ties),
records it and rewrites every word with a left-to-right, non-overlapping merge. Applying BPE replays
the merges in learned order on a new word.

## References

- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) — Rico Sennrich, Barry Haddow, Alexandra Birch (`S020`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)

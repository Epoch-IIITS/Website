# Byte-Pair Encoding (BPE)

## Learning outcomes

After this lesson you can:

- Count adjacent symbol pairs weighted by word frequency
- Learn BPE merges greedily
- Apply learned merges to segment a new word

## Intuition
Word-level vocabularies can't handle new words; character-level sequences are long. BPE starts
from characters and repeatedly glues together the most frequent adjacent pair, building a
vocabulary of useful subwords ("low", "est", "er").

## Precise explanation (Sennrich et al., 2016)
1. Represent each word as characters plus an end-of-word marker `</w>`: "low" → (l, o, w, </w>).
2. Count every adjacent symbol pair, weighted by word frequency.
3. Merge the most frequent pair everywhere it occurs (left to right, non-overlapping).
4. Repeat `num_merges` times (or until no pairs remain).
Ties: choose the lexicographically smallest pair (our deterministic choice; libraries differ).
**Applying** merges to a new word: start from characters + `</w>` and apply the learned merges
**in the order learned**.

## Worked example
counts {low: 5, lower: 2, newest: 6, widest: 3}: most frequent pair is (e, s) — appears in newest
(6) and widest (3) = 9 → merge "es"; next (es, t) = 9 → "est"; next (est, </w>) = 9 → "est</w>" …

## Common mistakes
* Not weighting pairs by word frequency.
* Merging overlapping pairs incorrectly ("aaa" with pair (a, a) → "aa a", not "a aa" twice).
* Applying merges in frequency order rather than learned order.

## Why this matters
GPT-style models use BPE variants (often on bytes); tokenisation affects cost (tokens per word),
perplexity comparisons and how models handle rare words.

## References

- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) — Rico Sennrich, Barry Haddow, Alexandra Birch (`S020`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)

# Character n-grams

## Learning outcomes

After this lesson you can:

- Extract character n-grams with boundary markers
- Generate ranges of n
- Compare words by n-gram overlap (Jaccard)

## Intuition
"running" and "runner" share the pieces "run" and "unn". Breaking words into overlapping
character chunks lets models relate words they've never seen together — and handle typos.

## Precise explanation
Wrap the word in boundary markers so prefixes and suffixes are distinguishable:
`"<" + word + ">"`. The character n-grams of a string $s$ are $s[i:i+n]$ for
$i = 0..|s|-n$. For "cat" with n = 3: "<cat>" → `<ca`, `cat`, `at>`.
A range $n_\text{min}..n_\text{max}$ concatenates all sizes (this is how fastText-style subword
features work). Words shorter than n (after markers) yield nothing for that n.

**Jaccard similarity** of two sets: $|A\cap B| / |A\cup B|$ (1 if both are empty, by convention
here).

## Worked example
"cat" vs "cart" (n = 3): {<ca, cat, at>} vs {<ca, car, art, rt>} → ∩ = {<ca}, ∪ has 6 →
J = 1/6.

## Common mistakes
* Forgetting the markers (then "at" inside "cat" and the word "at" look alike).
* Off-by-one: there are $|s| - n + 1$ n-grams.
* Treating repeated n-grams as distinct in Jaccard (use sets).

## Why this matters
Character and subword units (BPE, LM-06) are how modern language models avoid out-of-vocabulary
words.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) — Rico Sennrich, Barry Haddow, Alexandra Birch (`S020`)

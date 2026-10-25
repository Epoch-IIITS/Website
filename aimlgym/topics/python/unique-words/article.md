# Sets, Order and Normalisation

## Learning outcomes

After this lesson you can:

- Normalise tokens (case, punctuation)
- Use a set for fast membership
- Preserve first-occurrence order

## Intuition
A **set** remembers *whether* you have seen something, not *when*. To list unique words in the
order they first appeared, combine a set (fast "seen?" checks) with a list (keeps order).

## Precise explanation
* `set()` stores unique hashable items; `x in s` is on average O(1).
* Converting a list to a set loses order: `list(set(words))` may come back in any order.
* Pattern:
```python
seen, out = set(), []
for w in words:
    if w not in seen:
        seen.add(w)
        out.append(w)
```
* Normalisation: two tokens should count as the same word if they differ only in case or in
  surrounding punctuation. `w.strip(string.punctuation).lower()` removes punctuation from both
  ends only (so the apostrophe in "don't" survives).
* `str.split()` with no argument splits on any run of whitespace and drops empty strings.

## Worked example
`"The cat saw the CAT, then the dog."` → split → `The, cat, saw, the, CAT,, then, the, dog.` →
normalise → `the, cat, saw, the, cat, then, the, dog` → unique in order →
`['the', 'cat', 'saw', 'then', 'dog']`.

## Common mistakes
* `sorted(set(words))` — alphabetical, not first-occurrence order.
* `split(" ")` — produces empty strings for double spaces.
* Stripping *all* punctuation characters with `replace`, which turns "don't" into "dont".
* Keeping tokens that become empty after stripping (e.g. a lone "—").

## Why this matters
Building a vocabulary (word → index) for NLP models is exactly this operation; the order
determines each word's index, so it must be deterministic.

## Library implementation

Since Python 3.7 dictionaries keep insertion order, so `list(dict.fromkeys(words))` removes
duplicates while keeping first occurrences — a common one-line idiom once the words are
normalised. The set-plus-list loop makes the idea explicit; the test checks both agree.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)

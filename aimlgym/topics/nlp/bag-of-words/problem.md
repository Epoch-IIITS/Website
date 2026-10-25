# NL-07 · Bag-of-Words Vectors

**Topic:** Natural Language Processing · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NL-03 Counting Words with Counter and CountVectorizer

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `build_vocab(docs, min_count=1)` → dict word → index for words whose **total** count across all
  documents is `>= min_count`, indices assigned in alphabetical order.
* `vectorize(docs, vocab)` → int NumPy array `(len(docs), len(vocab))`; OOV tokens ignored.

`docs` is a list of token lists.

**Example**
```python
docs = [["a", "b", "a"], ["b", "c"]]
build_vocab(docs)              # {'a': 0, 'b': 1, 'c': 2}
vectorize(docs, build_vocab(docs))   # [[2, 1, 0], [0, 1, 1]]
build_vocab(docs, min_count=2) # {'a': 0, 'b': 1}
```

## Hints

<details><summary>Hint 1</summary>

`c = Counter(t for doc in docs for t in doc)`.

</details>

<details><summary>Hint 2</summary>

`words = sorted(w for w, k in c.items() if k >= min_count)`; enumerate them.

</details>

<details><summary>Hint 3</summary>

Loop documents and tokens; `if t in vocab: X[i, vocab[t]] += 1`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_vocab` | Assign indices in alphabetical order. |
| `test_min_count` | Filter by total count across all documents. |
| `test_oov` | Ignore tokens not in the vocabulary instead of raising KeyError. |
| `test_vectors` | Increment X[i, vocab[t]] for every token. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Counting all tokens once gives total frequencies for the `min_count` filter; sorting fixes the
column order. Vectorisation looks each token up and increments its column, skipping OOV words.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)

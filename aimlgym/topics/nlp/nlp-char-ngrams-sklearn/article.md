# Character n-grams with CountVectorizer

## Learning outcomes

After this lesson you can:

- Extract character n-grams with analyzer='char_wb'
- Compare strings that differ by typos with cosine similarity of n-gram counts
- Choose an ngram_range

## Intuition
"recieve" and "receive" share almost all of their three-letter pieces even though they are
different words. Counting **character n-grams** instead of words makes models robust to typos,
spelling variants and word endings, and works for languages without spaces.

## Precise explanation
```python
vec = CountVectorizer(analyzer="char_wb", ngram_range=(2, 3))
X = vec.fit_transform(["cat"])
vec.get_feature_names_out()     # [' c', ' ca', 'at', 'at ', 'ca', 'cat', 't ']
```

* `analyzer="char_wb"` takes n-grams **inside word boundaries** and pads each word with one space
  on both sides, so ' c' means "c at the start of a word". `analyzer="char"` runs across spaces.
* `ngram_range=(2, 3)` includes both bigrams and trigrams.
* Two texts are similar when their n-gram count vectors point the same way:
  `cosine_similarity(X[0], X[1])` from `sklearn.metrics.pairwise`, between 0 and 1 for counts.

## Worked example
With trigrams, "receive" and "recieve" share ' re', 'rec' and 've ' among their trigrams and
reach a cosine similarity well above that of "receive" and "banana".

## What the library does inside
It slides a window over each padded word — your NL-06, the optional deep dive after
this step — and counts the windows like words.

## Common mistakes
* Using `analyzer="char"` and getting n-grams that span two words.
* Very small n (1) that makes every text look alike, or large n (6+) that makes typos unmatched.
* Comparing vectors from two separately fitted vectorizers (different columns).

## Why this matters
Fuzzy name matching, spam detection with obfuscated words and language identification all use
character n-grams. NL-12 next measures edit distance directly.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)

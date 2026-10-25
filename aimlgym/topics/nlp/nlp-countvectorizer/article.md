# Counting Words with Counter and CountVectorizer

## Learning outcomes

After this lesson you can:

- Find the most common words with collections.Counter
- Turn documents into a word-count matrix with CountVectorizer
- Remove stop words and rare words with stop_words and min_df

## Intuition
The simplest description of a text is which words it uses and how often. For a quick look at one
corpus, `collections.Counter` counts tokens. For machine learning you need one row of counts per
document and one column per word — a **document–term matrix** — which `CountVectorizer` builds and
remembers, so new documents get the same columns.

## Precise explanation
```python
from collections import Counter
Counter(tokens).most_common(3)                 # [('the', 12), ('cat', 4), ...]

from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer(stop_words="english", min_df=2)
X = vec.fit_transform(docs)                    # sparse matrix (n_docs, n_words)
vec.get_feature_names_out()                    # the vocabulary, sorted alphabetically
vec.transform(["a new document"])              # same columns; unseen words are ignored
```

* Default tokenisation: lowercase, then the regex `\b\w\w+\b` — tokens of **two or more**
  word characters, so "a" and "I" disappear and punctuation splits words.
* `stop_words="english"` removes a built-in list of very common words ("the", "on", "and");
  a list of your own also works.
* `min_df=2` keeps words that appear in at least two documents (an int) or a fraction of them
  (a float); `max_df` drops words that appear almost everywhere.
* The result is a **sparse** matrix: most entries are zero. Use `.toarray()` only for small data.

## Worked example
For ["The cat sat on the mat", "The dog sat"], `CountVectorizer(stop_words="english")` learns the
vocabulary [cat, dog, mat, sat] and the matrix [[1, 0, 1, 1], [0, 1, 0, 1]].

## What the library does inside
Tokenise, filter and count — your NL-04 (the optional deep dive after this step) —
then store the vocabulary as a dict from word to column.

## Common mistakes
* Calling `fit_transform` on the test documents, which builds a different vocabulary.
* Being surprised that one-letter words vanish (the token pattern needs two characters).
* Converting a large sparse matrix with `.toarray()` and running out of memory.

## Why this matters
Count matrices feed TF-IDF, Naive Bayes and logistic-regression text classifiers in this topic.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)

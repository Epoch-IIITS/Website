# Stopwords and Frequencies

## Learning outcomes

After this lesson you can:

- Remove stopwords
- Count tokens with collections.Counter
- Return top-n words with deterministic tie-breaking

## Intuition
"the", "of" and "and" dominate any word count but say little about the topic. Removing these
**stopwords** lets content words rise to the top.

## Precise explanation
* A stopword list is a set of very common function words (NLTK ships lists for many languages).
  Use a `set` for O(1) membership.
* `collections.Counter(tokens)` counts occurrences.
* `Counter.most_common(n)` orders by count but ties keep first-encountered order, which depends on
  the text; sort explicitly with key `(-count, word)` for deterministic output.
* Stopword removal is task-dependent: for sentiment, "not" is crucial and should *not* be removed.

## Worked example
tokens [the, cat, and, the, hat, cat, sat], stopwords {the, and} →
[cat, hat, cat, sat] → top 2: [(cat, 2), (hat, 1)] (hat < sat alphabetically).

## Common mistakes
* Filtering with a list (slow for big vocabularies).
* Removing negations in sentiment tasks.
* Non-deterministic tie order.

## Why this matters
Frequency tables are the raw material of bag-of-words, TF-IDF and n-gram language models.

## Library implementation

`collections.Counter(tokens).most_common(n)` returns the top counts, but breaks ties by first
appearance rather than alphabetically, which is why this exercise sorts explicitly. NLTK and
spaCy ship curated stopword lists; scikit-learn's `CountVectorizer(stop_words="english")` uses
its own list. The test checks your counts against `Counter`.

## References

- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)

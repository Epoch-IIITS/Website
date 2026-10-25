# Bag of Words

## Learning outcomes

After this lesson you can:

- Build a vocabulary with a minimum count
- Map documents to count vectors
- Handle out-of-vocabulary tokens

## Intuition
Throw a document's words into a bag and count them, ignoring order. Each document becomes a
vector with one slot per vocabulary word. "dog bites man" and "man bites dog" get the same vector
— a known limitation.

## Precise explanation
* **Vocabulary:** map each word to a column index. Sort words alphabetically for a deterministic
  index. `min_count` drops rare words (typos, noise), shrinking the vector.
* **Vectorise:** `X[i, vocab[w]] += 1` for each token `w` of document `i`.
* **Out-of-vocabulary (OOV)** words at prediction time are ignored here (alternatives: an `<unk>`
  column).
* The matrix is mostly zeros; real libraries store it sparsely. Our tiny corpora fit in dense
  NumPy arrays.
* Build the vocabulary on **training** documents only (leakage again).

## Worked example
docs [[a, b, a], [b, c]], min_count 1 → vocab {a: 0, b: 1, c: 2} → X = [[2, 1, 0], [0, 1, 1]].
min_count 2 → vocab {a: 0, b: 1}.

## Common mistakes
* Vocabulary order depending on set iteration (non-deterministic).
* Counting document frequency instead of total count for `min_count` (here: total count).
* Crashing on unseen words.

## Why this matters
Bag-of-words feeds TF-IDF (NL-09), Naive Bayes (NL-14) and is the baseline any neural text model
should beat.

## Library implementation

scikit-learn's `CountVectorizer` builds the vocabulary and count matrix in one step (as a sparse
matrix). Passing `analyzer=lambda doc: doc` makes it accept pre-tokenised documents, and
`vocabulary=vocab` reuses your vocabulary. The comparison runs when scikit-learn is installed.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)

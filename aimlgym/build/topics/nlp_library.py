"""NLP with scikit-learn and PyTorch (library revision, Phase 4).

Library steps are followed by the by-hand versions they replace on the required path, kept as
optional deep dives: [[stopword-counts]], [[char-ngrams]], [[cosine-retrieval]]. [[bigram-counts]]
and [[suffix-stemmer]] are optional too (bigrams are counted again in [[bigram-next-token]]).
"""

TEXT_PACKAGES = ["numpy", "scikit-learn"]

REVIEWS = r'''
def reviews(seed=0, n=200):
    """Synthetic product reviews: positive and negative phrases mixed with neutral filler."""
    import random
    rng = random.Random(seed)
    good = ["great", "excellent", "love it", "works perfectly", "highly recommend", "fantastic", "very happy"]
    bad = ["terrible", "broke quickly", "waste of money", "very disappointed", "awful", "does not work", "poor quality"]
    filler = ["the phone", "this charger", "the delivery", "my order", "the battery", "the screen", "it", "the case"]
    texts, labels = [], []
    for i in range(n):
        label = i % 2
        words = rng.sample(good if label else bad, 2) + rng.sample(filler, 2)
        rng.shuffle(words)
        texts.append(" ".join(words))
        labels.append(label)
    return texts, labels
'''

PROBLEMS = [
# ---------------------------------------------------------------- nlp-countvectorizer
{
"slug": "nlp-countvectorizer", "title": "Counting Words with Counter and CountVectorizer",
"difficulty": "beginner", "prereqs": ["tokenize-normalize", "sklearn-estimator-api"], "packages": TEXT_PACKAGES,
"objectives": ["Find the most common words with collections.Counter",
               "Turn documents into a word-count matrix with CountVectorizer",
               "Remove stop words and rare words with stop_words and min_df"],
"tags": ["scikit-learn", "word-counts", "stop-words", "vectorisation"],
"sources": ["S126", "S012"], "entry": "top_words(texts, k, stop_words=()); count_matrix(texts, stop_words=None, min_df=1)",
"article": r'''
# Counting Words with Counter and CountVectorizer

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
Tokenise, filter and count — your [[stopword-counts]] (the optional deep dive after this step) —
then store the vocabulary as a dict from word to column.

## Common mistakes
* Calling `fit_transform` on the test documents, which builds a different vocabulary.
* Being surprised that one-letter words vanish (the token pattern needs two characters).
* Converting a large sparse matrix with `.toarray()` and running out of memory.

## Why this matters
Count matrices feed TF-IDF, Naive Bayes and logistic-regression text classifiers in this topic.
''',
"statement": r'''
1. `top_words(texts, k, stop_words=())` lowercases each text, finds tokens with
   `re.findall(r"[a-z']+", text.lower())`, drops tokens in `stop_words`, and returns the `k` most
   common as `(word, count)` pairs, sorted by count descending and then alphabetically.
2. `count_matrix(texts, stop_words=None, min_df=1)` fits `CountVectorizer(stop_words=stop_words,
   min_df=min_df)` and returns `(vocabulary, rows)`: the feature names as a list of strings and the
   dense matrix as a list of lists of ints.

Raise `ValueError` in both if `texts` is empty, and in `top_words` if `k < 1`.
''',
"starter": r'''
import re
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer


def top_words(texts, k, stop_words=()):
    # TODO
    pass


def count_matrix(texts, stop_words=None, min_df=1):
    # TODO
    pass
''',
"hints": [
    "Update one Counter with the filtered tokens of every text.",
    "`sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]` gives the ordering.",
    "`vec = CountVectorizer(...)`; `X = vec.fit_transform(texts)`; return `list(vec.get_feature_names_out())` and `X.toarray().tolist()`.",
],
"solution": r'''
import re
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer


def top_words(texts, k, stop_words=()):
    if not texts or k < 1:
        raise ValueError("need texts and k >= 1")
    stop = set(stop_words)
    counts = Counter()
    for text in texts:
        counts.update(t for t in re.findall(r"[a-z']+", text.lower()) if t not in stop)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def count_matrix(texts, stop_words=None, min_df=1):
    if not texts:
        raise ValueError("need at least one text")
    vec = CountVectorizer(stop_words=stop_words, min_df=min_df)
    X = vec.fit_transform(texts)
    return [str(w) for w in vec.get_feature_names_out()], X.toarray().tolist()
''',
"explanation": r'''
`Counter` accumulates token frequencies across all texts; sorting on negative count and then the
word gives a deterministic top-k. `CountVectorizer` learns the vocabulary and produces one count row
per document; its feature names are already in column order.
''',
"tests": r'''
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer


class TestCounting(unittest.TestCase):
    def test_count_matrix_example(self):
        vocab, rows = S.count_matrix(["The cat sat on the mat", "The dog sat"], stop_words="english")
        self.assertEqual(vocab, ["cat", "dog", "mat", "sat"])
        self.assertEqual(rows, [[1, 0, 1, 1], [0, 1, 0, 1]])

    def test_top_words(self):
        texts = ["the cat and the hat", "The cat sat", "a dog"]
        self.assertEqual(S.top_words(texts, 2), [("the", 3), ("cat", 2)])
        self.assertEqual(S.top_words(texts, 2, stop_words={"the", "and", "a"}), [("cat", 2), ("dog", 1)])

    def test_top_words_ties_alphabetical(self):
        self.assertEqual(S.top_words(["b a c", "c b a"], 3), [("a", 2), ("b", 2), ("c", 2)])

    def test_min_df(self):
        vocab, rows = S.count_matrix(["red apple", "green apple", "red car"], min_df=2)
        self.assertEqual(vocab, ["apple", "red"])
        self.assertEqual(rows, [[1, 1], [1, 0], [0, 1]])

    def test_single_letters_dropped_and_types(self):
        vocab, rows = S.count_matrix(["I saw a cat", "a cat saw me"])
        self.assertNotIn("i", vocab)
        self.assertNotIn("a", vocab)
        self.assertTrue(all(type(v) is int for row in rows for v in row))
        self.assertTrue(all(type(w) is str for w in vocab))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.count_matrix([])
        with self.assertRaises(ValueError):
            S.top_words(["x"], 0)
''',
"feedback": [
    ("test_count_matrix_example", "Fit CountVectorizer(stop_words=...) and return get_feature_names_out() and the dense rows."),
    ("test_top_words_ties_alphabetical", "Sort by (-count, word)."),
    ("test_min_df", "Pass min_df to CountVectorizer."),
    ("test_single_letters_dropped_and_types", "Return plain str and int values."),
],
},
# ---------------------------------------------------------------- nlp-char-ngrams-sklearn
{
"slug": "nlp-char-ngrams-sklearn", "title": "Character n-grams with CountVectorizer",
"difficulty": "beginner", "prereqs": ["nlp-countvectorizer"], "packages": TEXT_PACKAGES,
"objectives": ["Extract character n-grams with analyzer='char_wb'",
               "Compare strings that differ by typos with cosine similarity of n-gram counts",
               "Choose an ngram_range"],
"tags": ["scikit-learn", "character-ngrams", "fuzzy-matching", "cosine-similarity"],
"sources": ["S126", "S012"], "entry": "char_ngrams(texts, n_min=2, n_max=3); char_similarity(a, b, n=3)",
"article": r'''
# Character n-grams with CountVectorizer

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
It slides a window over each padded word — your [[char-ngrams]], the optional deep dive after
this step — and counts the windows like words.

## Common mistakes
* Using `analyzer="char"` and getting n-grams that span two words.
* Very small n (1) that makes every text look alike, or large n (6+) that makes typos unmatched.
* Comparing vectors from two separately fitted vectorizers (different columns).

## Why this matters
Fuzzy name matching, spam detection with obfuscated words and language identification all use
character n-grams. [[levenshtein]] next measures edit distance directly.
''',
"statement": r'''
1. `char_ngrams(texts, n_min=2, n_max=3)` fits `CountVectorizer(analyzer="char_wb", ngram_range=(n_min, n_max))`
   and returns `(features, rows)` as a list of strings and a list of int lists.
2. `char_similarity(a, b, n=3)` fits a char_wb vectorizer with `ngram_range=(n, n)` on `[a, b]` and
   returns their cosine similarity as a float.

Raise `ValueError` if `n_min < 1` or `n_min > n_max` (and for `n < 1`).
''',
"starter": r'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def char_ngrams(texts, n_min=2, n_max=3):
    # TODO
    pass


def char_similarity(a, b, n=3):
    # TODO
    pass
''',
"hints": [
    "Validate the n-gram sizes before building the vectorizer.",
    "`vec = CountVectorizer(analyzer=\"char_wb\", ngram_range=(n_min, n_max))`.",
    "`X = vec.fit_transform([a, b])`; `float(cosine_similarity(X[0], X[1])[0, 0])`.",
],
"solution": r'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def char_ngrams(texts, n_min=2, n_max=3):
    if n_min < 1 or n_min > n_max:
        raise ValueError("need 1 <= n_min <= n_max")
    vec = CountVectorizer(analyzer="char_wb", ngram_range=(n_min, n_max))
    X = vec.fit_transform(texts)
    return [str(f) for f in vec.get_feature_names_out()], X.toarray().tolist()


def char_similarity(a, b, n=3):
    if n < 1:
        raise ValueError("n must be at least 1")
    X = CountVectorizer(analyzer="char_wb", ngram_range=(n, n)).fit_transform([a, b])
    return float(cosine_similarity(X[0], X[1])[0, 0])
''',
"explanation": r'''
`char_wb` pads every word with spaces and counts the n-grams inside it. Fitting both strings in one
vectorizer guarantees that their count vectors share columns, so the cosine similarity compares like
with like.
''',
"tests": r'''
class TestCharNgrams(unittest.TestCase):
    def test_cat_bigrams(self):
        features, rows = S.char_ngrams(["cat"], 2, 2)
        self.assertEqual(features, [" c", "at", "ca", "t "])
        self.assertEqual(rows, [[1, 1, 1, 1]])

    def test_range_includes_both_sizes(self):
        features, _ = S.char_ngrams(["cat"], 2, 3)
        self.assertEqual(features, [" c", " ca", "at", "at ", "ca", "cat", "t "])

    def test_word_boundaries(self):
        features, _ = S.char_ngrams(["ab cd"], 2, 2)
        self.assertEqual(features, [" a", " c", "ab", "b ", "cd", "d "])

    def test_typo_closer_than_unrelated(self):
        typo = S.char_similarity("receive", "recieve")
        other = S.char_similarity("receive", "banana")
        self.assertGreater(typo, 0.3)
        self.assertLess(other, 0.1)

    def test_identical_and_type(self):
        self.assertAlmostEqual(S.char_similarity("hello", "hello"), 1.0)
        self.assertIs(type(S.char_similarity("a b", "b a")), float)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.char_ngrams(["x"], 3, 2)
        with self.assertRaises(ValueError):
            S.char_similarity("a", "b", 0)
''',
"feedback": [
    ("test_cat_bigrams", "Use analyzer='char_wb', which pads words with spaces."),
    ("test_range_includes_both_sizes", "ngram_range=(n_min, n_max)."),
    ("test_typo_closer_than_unrelated", "Fit one vectorizer on both strings and use cosine_similarity."),
    ("test_invalid", "Reject n_min < 1, n_min > n_max and n < 1."),
],
},
# ---------------------------------------------------------------- nlp-tfidf-retrieval
{
"slug": "nlp-tfidf-retrieval", "title": "Search with TfidfVectorizer and Cosine Similarity",
"difficulty": "intermediate", "prereqs": ["tf-idf"], "packages": TEXT_PACKAGES,
"objectives": ["Index documents with TfidfVectorizer",
               "Rank documents for a query with cosine_similarity",
               "Explain why TF-IDF rows are L2-normalised"],
"tags": ["scikit-learn", "tf-idf", "information-retrieval", "search"],
"sources": ["S126", "S012"], "entry": "build_index(docs); search(index, query, k=3)",
"article": r'''
# Search with TfidfVectorizer and Cosine Similarity

## Intuition
A search engine needs a score for "how well does this document match the query?". TF-IDF weights
words that are frequent in a document but rare in the collection; cosine similarity compares the
query's weights with each document's. Rank by score and show the top few.

## Precise explanation
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vec = TfidfVectorizer()
D = vec.fit_transform(docs)                 # one L2-normalised row per document
q = vec.transform([query])                  # same vocabulary and IDF weights
scores = cosine_similarity(q, D)[0]         # one score per document
```

* scikit-learn's IDF is smoothed: idf(t) = ln((1 + n)/(1 + df(t))) + 1, so every word keeps a
  positive weight. Rows are L2-normalised (`norm="l2"`), which makes cosine similarity a plain dot
  product.
* The query is **transformed**, never fitted: it must use the documents' vocabulary and IDF.
* A query of only unknown words gets a zero vector and scores 0 against everything.

## Worked example
Documents "python lists are mutable", "tuples are immutable", "pandas dataframes hold tables":
the query "mutable lists" scores highest on the first document; "are" appears in two documents, so
it has a lower IDF and contributes less.

## What the library does inside
The TF-IDF weighting of [[tf-idf]] and the cosine ranking of [[cosine-retrieval]] (the optional
deep dive after this step), on sparse matrices so that millions of documents are feasible.

## Common mistakes
* Fitting a new vectorizer on the query.
* Forgetting that `cosine_similarity` returns a 2-D array (one row per query).
* Breaking ties arbitrarily; sort by score and then by document index for stable results.

## Why this matters
This is the retrieval step of the RAG pipeline in the LLM topic and the basis of the blog
semantic-search project idea.
''',
"statement": r'''
1. `build_index(docs)` returns `(vectorizer, matrix)` from `TfidfVectorizer().fit_transform(docs)`.
   Raise `ValueError` for an empty list.
2. `search(index, query, k=3)` returns up to `k` pairs `(doc_index, score)` sorted by score
   descending and then index ascending, with scores as floats from `cosine_similarity`. Raise
   `ValueError` if `k < 1`.
''',
"starter": r'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_index(docs):
    # TODO
    pass


def search(index, query, k=3):
    # TODO
    pass
''',
"hints": [
    "`vec = TfidfVectorizer(); matrix = vec.fit_transform(docs)`.",
    "`scores = cosine_similarity(vec.transform([query]), matrix)[0]`.",
    "`sorted(range(len(scores)), key=lambda i: (-scores[i], i))[:k]`.",
],
"solution": r'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_index(docs):
    if not docs:
        raise ValueError("need at least one document")
    vec = TfidfVectorizer()
    return vec, vec.fit_transform(docs)


def search(index, query, k=3):
    if k < 1:
        raise ValueError("k must be at least 1")
    vec, matrix = index
    scores = cosine_similarity(vec.transform([query]), matrix)[0]
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))[:k]
    return [(i, float(scores[i])) for i in order]
''',
"explanation": r'''
The index stores the fitted vectorizer and the document matrix. A query is transformed with the
same vocabulary and IDF; cosine similarity scores it against every document, and a stable sort
returns the best matches first.
''',
"tests": r'''
import numpy as np


DOCS = ["python lists are mutable", "tuples are immutable", "pandas dataframes hold tables",
        "lists and tuples are sequences"]


class TestTfidfSearch(unittest.TestCase):
    def test_best_match_first(self):
        index = S.build_index(DOCS)
        self.assertEqual(S.search(index, "mutable lists", k=1)[0][0], 0)
        self.assertEqual(S.search(index, "pandas tables", k=1)[0][0], 2)

    def test_scores_sorted_and_bounded(self):
        results = S.search(S.build_index(DOCS), "lists tuples", k=4)
        scores = [s for _, s in results]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertTrue(all(0.0 <= s <= 1.0 + 1e-9 for s in scores))
        self.assertEqual(results[0][0], 3)

    def test_rows_normalised(self):
        _, matrix = S.build_index(DOCS)
        self.assertTrue(np.allclose(np.linalg.norm(matrix.toarray(), axis=1), 1.0))

    def test_unknown_words(self):
        results = S.search(S.build_index(DOCS), "quantum chromodynamics", k=2)
        self.assertEqual(results, [(0, 0.0), (1, 0.0)])

    def test_k_larger_than_corpus(self):
        results = S.search(S.build_index(DOCS[:2]), "immutable", k=10)
        self.assertEqual(len(results), 2)
        self.assertIs(type(results[0][1]), float)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.build_index([])
        with self.assertRaises(ValueError):
            S.search(S.build_index(DOCS), "x", k=0)
''',
"feedback": [
    ("test_best_match_first", "Transform the query with the fitted vectorizer; do not fit a new one."),
    ("test_scores_sorted_and_bounded", "Sort by score descending, then by index."),
    ("test_unknown_words", "Unknown words give zero scores; ties keep index order."),
    ("test_invalid", "Reject an empty corpus and k < 1."),
],
},
# ---------------------------------------------------------------- nlp-text-classifier
{
"slug": "nlp-text-classifier", "title": "A Text Classification Pipeline",
"difficulty": "advanced", "prereqs": ["naive-bayes-text", "nlp-tfidf-retrieval"], "packages": TEXT_PACKAGES,
"objectives": ["Build a TfidfVectorizer + LogisticRegression pipeline for raw text",
               "Use word bigrams and sublinear term frequency",
               "Read the most informative words from the model's coefficients"],
"tags": ["scikit-learn", "text-classification", "sentiment-analysis", "tf-idf", "logistic-regression"],
"sources": ["S126", "S091"], "entry": "train_text_classifier(texts, labels, C=1.0); top_features(pipe, n=5)",
"article": r'''
# A Text Classification Pipeline

## Intuition
Sentiment, spam, topic labels: most text classification starts with the same strong baseline —
TF-IDF features and a linear classifier. Because the model is linear, each word gets a weight, and
the largest weights show what the model has learned.

## Precise explanation
```python
pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
    ("clf", LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(train_texts, train_labels)
pipe.predict(["the battery died after a day"])
```

* The pipeline takes **raw strings**: the vectorizer is fitted inside `fit`, so cross-validation and
  grid search never leak test vocabulary ([[sklearn-scaler-pipeline]]).
* `ngram_range=(1, 2)` adds word pairs, so "not good" becomes a feature of its own.
* `sublinear_tf=True` uses 1 + log(tf), so a word repeated ten times does not count ten times as much.
* For binary labels, `clf.coef_[0]` has one weight per feature; positive weights push towards
  class 1. `pipe.named_steps["tfidf"].get_feature_names_out()` gives the matching words.
* `C` is the inverse regularisation strength ([[sklearn-grid-search]]).

## Worked example
Trained on product reviews, the largest positive weights go to "great", "love it", "highly
recommend"; the most negative to "terrible", "broke quickly", "waste of money".

## What the library does inside
The vectorizer is the TF-IDF of [[nlp-tfidf-retrieval]]; logistic regression is the model you built
in [[logistic-regression]], optimised with a quasi-Newton solver.

## Common mistakes
* Vectorising all texts before splitting.
* Reading weights from a model trained on unscaled counts (TF-IDF keeps them comparable).
* Assuming a word's weight is its effect in every context; correlated phrases share weight.

## Why this matters
This pipeline is often within a few points of far larger models, trains in seconds and explains
itself — a good first model for the review-sentiment project idea after this step.
''',
"statement": r'''
1. `train_text_classifier(texts, labels, C=1.0)` fits and returns
   `Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)), ("clf", LogisticRegression(C=C, max_iter=1000))])`.
   Raise `ValueError` if the lengths differ or there are fewer than two classes.
2. `top_features(pipe, n=5)` for a binary pipeline returns `{"positive": [...], "negative": [...]}`:
   the `n` features with the largest and with the most negative coefficients, each list ordered from
   strongest to weakest.
''',
"starter": r'''
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def train_text_classifier(texts, labels, C=1.0):
    # TODO
    pass


def top_features(pipe, n=5):
    # TODO
    pass
''',
"hints": [
    "Validate `len(texts) == len(labels)` and `len(set(labels)) >= 2`, then build and fit the pipeline.",
    "`names = pipe.named_steps[\"tfidf\"].get_feature_names_out()`; `weights = pipe.named_steps[\"clf\"].coef_[0]`.",
    "`order = np.argsort(weights)`: the last n reversed are positive, the first n are negative.",
],
"solution": r'''
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def train_text_classifier(texts, labels, C=1.0):
    if len(texts) != len(labels) or len(set(labels)) < 2:
        raise ValueError("need matching texts and labels with at least two classes")
    pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
                     ("clf", LogisticRegression(C=C, max_iter=1000))])
    return pipe.fit(texts, labels)


def top_features(pipe, n=5):
    names = pipe.named_steps["tfidf"].get_feature_names_out()
    weights = pipe.named_steps["clf"].coef_[0]
    order = np.argsort(weights, kind="stable")
    return {"positive": [str(names[i]) for i in order[::-1][:n]],
            "negative": [str(names[i]) for i in order[:n]]}
''',
"explanation": r'''
The pipeline learns the vocabulary and the weights together from raw text. For a binary model each
coefficient belongs to one word or word pair; sorting them shows the phrases that most strongly
indicate each class.
''',
"tests": r'''
import numpy as np
''' + REVIEWS + r'''

class TestTextClassifier(unittest.TestCase):
    def test_accuracy_on_new_reviews(self):
        texts, labels = reviews(0)
        pipe = S.train_text_classifier(texts, labels)
        test_texts, test_labels = reviews(1, 100)
        self.assertGreater(np.mean(pipe.predict(test_texts) == np.array(test_labels)), 0.95)

    def test_pipeline_structure(self):
        texts, labels = reviews(2, 40)
        pipe = S.train_text_classifier(texts, labels, C=3.0)
        self.assertEqual(list(pipe.named_steps), ["tfidf", "clf"])
        self.assertEqual(pipe.named_steps["tfidf"].ngram_range, (1, 2))
        self.assertTrue(pipe.named_steps["tfidf"].sublinear_tf)
        self.assertEqual(pipe.named_steps["clf"].C, 3.0)

    def test_top_features_make_sense(self):
        texts, labels = reviews(3)
        top = S.top_features(S.train_text_classifier(texts, labels), n=8)
        good = {"great", "excellent", "love", "love it", "fantastic", "happy", "very happy", "recommend", "highly", "highly recommend", "perfectly", "works perfectly", "works"}
        bad = {"terrible", "awful", "broke", "broke quickly", "quickly", "waste", "money", "waste of", "of money", "disappointed", "very disappointed", "poor", "quality", "poor quality", "does", "not", "work", "does not", "not work"}
        self.assertGreater(len(set(top["positive"]) & good), 4)
        self.assertGreater(len(set(top["negative"]) & bad), 4)

    def test_top_features_order_and_types(self):
        texts, labels = reviews(4, 60)
        pipe = S.train_text_classifier(texts, labels)
        top = S.top_features(pipe, n=3)
        names = list(pipe.named_steps["tfidf"].get_feature_names_out())
        w = pipe.named_steps["clf"].coef_[0]
        pos = [w[names.index(t)] for t in top["positive"]]
        self.assertEqual(pos, sorted(pos, reverse=True))
        self.assertTrue(all(type(t) is str for t in top["positive"] + top["negative"]))

    def test_probabilities(self):
        texts, labels = reviews(5, 60)
        proba = S.train_text_classifier(texts, labels).predict_proba(["great and fantastic", "awful and terrible"])
        self.assertTrue(np.allclose(proba.sum(axis=1), 1))
        self.assertGreater(proba[0, 1], proba[1, 1])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.train_text_classifier(["a b", "c d"], [1, 1])
        with self.assertRaises(ValueError):
            S.train_text_classifier(["a b"], [0, 1])
''',
"feedback": [
    ("test_accuracy_on_new_reviews", "Fit a Pipeline of TfidfVectorizer and LogisticRegression on the raw texts."),
    ("test_pipeline_structure", "Use ngram_range=(1, 2), sublinear_tf=True and the given C."),
    ("test_top_features_make_sense", "Positive coefficients point to class 1; sort coef_[0]."),
    ("test_invalid", "Require matching lengths and at least two classes."),
],
},
# ---------------------------------------------------------------- nlp-error-analysis
{
"slug": "nlp-error-analysis", "title": "Evaluating Text Classifiers",
"difficulty": "advanced", "prereqs": ["nlp-text-classifier"], "packages": TEXT_PACKAGES,
"objectives": ["Report per-class precision, recall and F1 with classification_report",
               "Read a confusion matrix for several classes",
               "Collect misclassified examples for error analysis"],
"tags": ["scikit-learn", "evaluation", "error-analysis", "confusion-matrix", "f1"],
"sources": ["S091", "S126"], "entry": "error_report(texts, y_true, y_pred, labels)",
"article": r'''
# Evaluating Text Classifiers

## Intuition
One accuracy number hides where a model fails. With several classes, look at precision and recall
per class, at which classes are confused with which, and at the actual misclassified texts — they
usually reveal the fix (missing negations, sarcasm, a mislabelled training example, a new topic).

## Precise explanation
```python
from sklearn.metrics import classification_report, confusion_matrix
confusion_matrix(y_true, y_pred, labels=labels)      # rows: true class, columns: predicted
classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
```

* Row i, column j of the confusion matrix counts examples of class labels[i] predicted as labels[j];
  the diagonal is correct predictions.
* `output_dict=True` returns per-class dicts with `precision`, `recall`, `f1-score` and `support`,
  plus `"macro avg"` (unweighted mean over classes) and `"weighted avg"`.
* **Macro F1** treats every class equally — important when classes are imbalanced, since a model can
  reach high accuracy by ignoring a rare class.
* `zero_division=0` avoids warnings for classes that are never predicted.

## Worked example
For true [pos, pos, neg, neu] and predicted [pos, neg, neg, neg] with labels [neg, neu, pos]: the
confusion matrix is [[1, 0, 0], [1, 0, 0], [1, 0, 1]]; neutral has recall 0, and the errors are the
second and fourth texts.

## Common mistakes
* Reading the confusion matrix with rows and columns swapped.
* Reporting weighted averages only, which hide poor minority classes.
* Fixing errors by editing the test set rather than understanding them.

## Why this matters
Error analysis decides what to do next — more data for a class, new features, or relabelling — and
is a standard part of every model report.
''',
"statement": r'''
Write `error_report(texts, y_true, y_pred, labels)` returning

* `"confusion"`: `confusion_matrix(y_true, y_pred, labels=labels)` as a list of int lists;
* `"per_class"`: `{label: {"precision": float, "recall": float, "f1": float, "support": int}}` from
  `classification_report(..., labels=labels, output_dict=True, zero_division=0)`;
* `"macro_f1"`: the report's `"macro avg"` F1 as a float;
* `"errors"`: `(text, true_label, predicted_label)` tuples for every misclassified example, in input order.

Raise `ValueError` if the three sequences differ in length.
''',
"starter": r'''
from sklearn.metrics import classification_report, confusion_matrix


def error_report(texts, y_true, y_pred, labels):
    # TODO
    pass
''',
"hints": [
    "Check that the three lengths match.",
    "`report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)`; per-class entries are keyed by `str(label)`.",
    "Errors: `[(t, a, b) for t, a, b in zip(texts, y_true, y_pred) if a != b]`.",
],
"solution": r'''
from sklearn.metrics import classification_report, confusion_matrix


def error_report(texts, y_true, y_pred, labels):
    if not len(texts) == len(y_true) == len(y_pred):
        raise ValueError("texts, y_true and y_pred must have the same length")
    report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
    per_class = {}
    for label in labels:
        row = report[str(label)]
        per_class[label] = {"precision": float(row["precision"]), "recall": float(row["recall"]),
                            "f1": float(row["f1-score"]), "support": int(row["support"])}
    return {"confusion": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
            "per_class": per_class, "macro_f1": float(report["macro avg"]["f1-score"]),
            "errors": [(t, a, b) for t, a, b in zip(texts, y_true, y_pred) if a != b]}
''',
"explanation": r'''
The confusion matrix and the report come straight from `sklearn.metrics` with a fixed label order,
so rows, columns and per-class entries line up. Collecting the misclassified texts beside their true
and predicted labels gives the material for error analysis.
''',
"tests": r'''
from sklearn.metrics import f1_score, precision_score, recall_score


TEXTS = ["love it", "fine I guess", "awful", "it is ok", "great value", "not great"]
TRUE = ["pos", "neu", "neg", "neu", "pos", "neg"]
PRED = ["pos", "neg", "neg", "neu", "pos", "pos"]
LABELS = ["neg", "neu", "pos"]


class TestErrorReport(unittest.TestCase):
    def test_worked_example(self):
        r = S.error_report(["a", "b", "c", "d"], ["pos", "pos", "neg", "neu"], ["pos", "neg", "neg", "neg"], LABELS)
        self.assertEqual(r["confusion"], [[1, 0, 0], [1, 0, 0], [1, 0, 1]])
        self.assertEqual(r["per_class"]["neu"]["recall"], 0.0)
        self.assertEqual([e[0] for e in r["errors"]], ["b", "d"])

    def test_per_class_matches_metrics(self):
        r = S.error_report(TEXTS, TRUE, PRED, LABELS)
        p = precision_score(TRUE, PRED, labels=LABELS, average=None, zero_division=0)
        rc = recall_score(TRUE, PRED, labels=LABELS, average=None, zero_division=0)
        for i, label in enumerate(LABELS):
            self.assertAlmostEqual(r["per_class"][label]["precision"], p[i])
            self.assertAlmostEqual(r["per_class"][label]["recall"], rc[i])
            self.assertEqual(r["per_class"][label]["support"], TRUE.count(label))

    def test_macro_f1(self):
        r = S.error_report(TEXTS, TRUE, PRED, LABELS)
        self.assertAlmostEqual(r["macro_f1"], f1_score(TRUE, PRED, labels=LABELS, average="macro"))

    def test_errors_in_order(self):
        r = S.error_report(TEXTS, TRUE, PRED, LABELS)
        self.assertEqual(r["errors"], [("fine I guess", "neu", "neg"), ("not great", "neg", "pos")])

    def test_label_order_controls_matrix(self):
        r = S.error_report(TEXTS, TRUE, PRED, ["pos", "neu", "neg"])
        self.assertEqual(r["confusion"][0], [2, 0, 0])
        self.assertTrue(all(type(v) is int for row in r["confusion"] for v in row))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.error_report(["a"], ["pos", "neg"], ["pos", "neg"], LABELS)
''',
"feedback": [
    ("test_worked_example", "Rows of the confusion matrix are true labels, columns predicted, in the given label order."),
    ("test_per_class_matches_metrics", "Read precision, recall, f1-score and support from classification_report(output_dict=True)."),
    ("test_errors_in_order", "Keep (text, true, predicted) for mismatches in input order."),
    ("test_invalid", "All three sequences must have the same length."),
],
},
# ---------------------------------------------------------------- nlp-embedding-bag
{
"slug": "nlp-embedding-bag", "title": "Word Embeddings in PyTorch",
"difficulty": "advanced", "prereqs": ["embedding-analogy", "torch-training-loop"], "packages": ["torch"],
"objectives": ["Map tokens to integer ids with a vocabulary that has an unknown token",
               "Average learned word embeddings with nn.EmbeddingBag and offsets",
               "Train an embedding-bag classifier end to end"],
"tags": ["pytorch", "embeddings", "text-classification", "embedding-bag"],
"sources": ["S127", "S039"], "entry": "build_vocab(texts, min_count=1); encode(texts, vocab); class BagClassifier(nn.Module); train_bag(texts, labels, dim=16, epochs=30, lr=0.05, seed=0)",
"article": r'''
# Word Embeddings in PyTorch

## Intuition
PPMI vectors ([[ppmi-matrix]]) are computed from counts. A neural model can instead **learn** a
small dense vector for every word, tuned for the task at hand. The simplest such model averages the
vectors of a text's words and feeds the average to a linear classifier — fast, and surprisingly strong.

## Precise explanation
1. **Vocabulary**: id 0 is `"<unk>"` for unseen words; other words get ids by frequency (descending),
   ties alphabetically.
2. **Encoding** many texts of different lengths as one flat tensor of ids plus **offsets** — the
   position where each text starts:

   texts ["good phone", "bad"] → ids [g, p, b], offsets [0, 2].
3. **Model**:

```python
self.embedding = nn.EmbeddingBag(vocab_size, dim, mode="mean")   # averages each bag of ids
self.fc = nn.Linear(dim, n_classes)
def forward(self, ids, offsets):
    return self.fc(self.embedding(ids, offsets))
```

* `nn.EmbeddingBag` is an `nn.Embedding` lookup followed by a mean, without padding.
* An empty text is an empty bag; its mean is a zero vector.
* After training, words used in similar ways end up with similar vectors.

## Worked example
With vocab {<unk>: 0, phone: 1, good: 2, bad: 3}, "good phone" and "bad" encode to ids
[2, 1, 3] and offsets [0, 2]; "excellent phone" becomes [0, 1] because "excellent" is unknown.

## Common mistakes
* Forgetting the unknown token, so new words crash the lookup.
* Offsets that count from 1 or give lengths instead of start positions.
* Building the vocabulary on test texts.

## Why this matters
Learned embeddings are the input layer of every language model; the token and position embeddings
of the transformer in the LLM topic work the same way.
''',
"statement": r'''
1. `build_vocab(texts, min_count=1)` splits lowercased texts on whitespace and returns a dict with
   `"<unk>": 0` and words with count ≥ `min_count` numbered from 1 by count descending, then
   alphabetically.
2. `encode(texts, vocab)` returns `(ids, offsets)` as `torch.long` tensors, mapping unknown words to 0.
3. `class BagClassifier(nn.Module)` with `__init__(self, vocab_size, dim, n_classes)` storing
   `self.embedding = nn.EmbeddingBag(vocab_size, dim, mode="mean")` and `self.fc = nn.Linear(dim, n_classes)`;
   `forward(ids, offsets)`.
4. `train_bag(texts, labels, dim=16, epochs=30, lr=0.05, seed=0)` builds the vocabulary, calls
   `torch.manual_seed(seed)`, creates the model and trains on the **whole set each epoch** (one batch)
   with Adam and `CrossEntropyLoss`. Return `(model, vocab, history)` with the model in `eval()` mode.
''',
"starter": r'''
from collections import Counter

import torch
from torch import nn


def build_vocab(texts, min_count=1):
    # TODO
    pass


def encode(texts, vocab):
    # TODO
    pass


class BagClassifier(nn.Module):
    def __init__(self, vocab_size, dim, n_classes):
        super().__init__()
        # TODO

    def forward(self, ids, offsets):
        # TODO
        pass


def train_bag(texts, labels, dim=16, epochs=30, lr=0.05, seed=0):
    # TODO
    pass
''',
"hints": [
    "Vocabulary: `Counter` over all words, keep those with enough counts, sort by `(-count, word)`, and number from 1.",
    "Encode: extend one list of ids per text, recording `len(ids)` before each text as its offset.",
    "Training: one forward pass on all texts per epoch — `loss = loss_fn(model(ids, offsets), y)`.",
],
"solution": r'''
from collections import Counter

import torch
from torch import nn


def build_vocab(texts, min_count=1):
    counts = Counter(w for text in texts for w in text.lower().split())
    words = sorted((w for w, c in counts.items() if c >= min_count), key=lambda w: (-counts[w], w))
    vocab = {"<unk>": 0}
    for i, w in enumerate(words, 1):
        vocab[w] = i
    return vocab


def encode(texts, vocab):
    ids, offsets = [], []
    for text in texts:
        offsets.append(len(ids))
        ids.extend(vocab.get(w, 0) for w in text.lower().split())
    return torch.tensor(ids, dtype=torch.long), torch.tensor(offsets, dtype=torch.long)


class BagClassifier(nn.Module):
    def __init__(self, vocab_size, dim, n_classes):
        super().__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, dim, mode="mean")
        self.fc = nn.Linear(dim, n_classes)

    def forward(self, ids, offsets):
        return self.fc(self.embedding(ids, offsets))


def train_bag(texts, labels, dim=16, epochs=30, lr=0.05, seed=0):
    vocab = build_vocab(texts)
    ids, offsets = encode(texts, vocab)
    y = torch.as_tensor(labels, dtype=torch.long)
    torch.manual_seed(seed)
    model = BagClassifier(len(vocab), dim, int(y.max()) + 1)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = []
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        loss = loss_fn(model(ids, offsets), y)
        loss.backward()
        opt.step()
        history.append(loss.item())
    model.eval()
    return model, vocab, history
''',
"explanation": r'''
The vocabulary reserves id 0 for unknown words so any text can be encoded. Concatenating ids and
recording where each text starts lets `EmbeddingBag` average variable-length texts without padding.
The classifier learns the embeddings and the output layer together.
''',
"tests": r'''
import numpy as np
import torch
''' + REVIEWS + r'''

class TestEmbeddingBag(unittest.TestCase):
    def test_vocab_order(self):
        vocab = S.build_vocab(["b a", "a c", "a b"])
        self.assertEqual(vocab, {"<unk>": 0, "a": 1, "b": 2, "c": 3})
        self.assertEqual(S.build_vocab(["x y x"], min_count=2), {"<unk>": 0, "x": 1})

    def test_encode_offsets_and_unknown(self):
        vocab = {"<unk>": 0, "phone": 1, "good": 2, "bad": 3}
        ids, offsets = S.encode(["good phone", "bad", "excellent phone"], vocab)
        self.assertEqual(ids.tolist(), [2, 1, 3, 0, 1])
        self.assertEqual(offsets.tolist(), [0, 2, 3])
        self.assertEqual((ids.dtype, offsets.dtype), (torch.long, torch.long))

    def test_model_output_and_mean(self):
        torch.manual_seed(0)
        model = S.BagClassifier(5, 4, 2)
        out = model(torch.tensor([1, 2, 3]), torch.tensor([0, 2]))
        self.assertEqual(tuple(out.shape), (2, 2))
        emb = model.embedding.weight
        expected = model.fc((emb[1] + emb[2]) / 2)
        self.assertTrue(torch.allclose(out[0], expected, atol=1e-6))

    def test_learns_reviews(self):
        texts, labels = reviews(0)
        model, vocab, history = S.train_bag(texts, labels, epochs=40)
        test_texts, test_labels = reviews(1, 100)
        ids, offsets = S.encode(test_texts, vocab)
        with torch.no_grad():
            preds = model(ids, offsets).argmax(dim=1).numpy()
        self.assertGreater(np.mean(preds == np.array(test_labels)), 0.9)
        self.assertLess(history[-1], history[0])

    def test_reproducible_and_eval(self):
        texts, labels = reviews(2, 40)
        a = S.train_bag(texts, labels, epochs=5, seed=1)
        b = S.train_bag(texts, labels, epochs=5, seed=1)
        self.assertEqual(a[2], b[2])
        self.assertFalse(a[0].training)

    def test_empty_text_is_zero_bag(self):
        model = S.BagClassifier(3, 2, 2)
        ids, offsets = S.encode(["", "a"], {"<unk>": 0, "a": 1})
        out = model.embedding(ids, offsets)
        self.assertEqual(out[0].tolist(), [0.0, 0.0])
''',
"feedback": [
    ("test_vocab_order", "Reserve 0 for <unk>, then number words by (-count, word)."),
    ("test_encode_offsets_and_unknown", "Offsets are start positions; unknown words map to 0."),
    ("test_model_output_and_mean", "Use nn.EmbeddingBag(vocab_size, dim, mode='mean') followed by nn.Linear."),
    ("test_reproducible_and_eval", "Seed before creating the model and finish in eval() mode."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "review-sentiment-analyser", "title": "Review Sentiment Analyser",
"tags": ["sentiment-analysis", "text-classification"],
"brief": r'''
Build a sentiment analyser for product or movie reviews that predicts positive or negative, explains
its decision with the words that mattered, and reports honestly where it fails (negation, sarcasm,
mixed reviews).
''',
"uses": ["nlp-countvectorizer", "nlp-tfidf-retrieval", "nlp-text-classifier", "sklearn-cross-validation"],
"milestones": [
    "Load a labelled review dataset and look at the class balance and typical review length.",
    "Train the TF-IDF + logistic regression pipeline and report cross-validated accuracy and F1.",
    "List the top positive and negative phrases and check that they make sense.",
    "Write an explain(review) function that shows each word's contribution to the score.",
    "Collect 30 misclassified reviews and group them by cause (negation, sarcasm, wrong label, ...).",
],
"stretch": [
    "Compare with the embedding-bag model in PyTorch.",
    "Add a third class for neutral or mixed reviews.",
    "Serve the model with FastAPI as in the 'Serve your model' project.",
],
"data": r'''
* IMDB movie reviews (50,000, balanced): on [Hugging Face](https://huggingface.co/datasets/stanfordnlp/imdb)
  or [Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews).
* Or write 100 short reviews of things you own and label them yourself.
''',
"setup": r'''
```bash
pip install scikit-learn pandas datasets
python sentiment.py
```
''',
},
{
"kind": "project", "slug": "blog-semantic-search", "title": "Semantic Search for the Club Blog",
"tags": ["search", "embeddings", "retrieval"],
"brief": r'''
Build a search box for a collection of blog posts that finds posts by meaning, not only exact words:
"beginner python workshop" should also find "Intro to programming session". Compare keyword (TF-IDF)
search with embedding-based search on the same queries.
''',
"uses": ["nlp-tfidf-retrieval", "nlp-char-ngrams-sklearn", "embedding-analogy", "nlp-embedding-bag"],
"milestones": [
    "Collect 50–200 posts (titles and text) into a JSON file.",
    "Build TF-IDF search and a small command-line interface that prints the top five results.",
    "Write 20 test queries with the posts you expect, and measure how often the right post is in the top three.",
    "Add character n-gram search for typos and compare the scores.",
    "Add embedding search with a sentence-embedding model and combine it with TF-IDF (for example by averaging ranks).",
],
"stretch": [
    "Add filters (author, date, tag) alongside the text search.",
    "Highlight the matching sentences in each result.",
    "Expose the search as a FastAPI endpoint for the website.",
],
"data": r'''
Use the Epoch blog posts you can access, or any set of articles you write or collect. Sentence-embedding
models such as those in the `sentence-transformers` library download weights the first time they run.
''',
"setup": r'''
```bash
pip install scikit-learn numpy sentence-transformers
python search.py "beginner python workshop"
```
''',
},
]

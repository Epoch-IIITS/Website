"""Problem definitions for the nlp topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- tokenize-normalize
{
"slug": "tokenize-normalize", "title": "Tokenize and Normalize",
"difficulty": "beginner", "prereqs": ["regex-text"], "packages": [],
"objectives": ["Normalise Unicode text (case, accents)", "Tokenise with a regular expression",
               "Keep contractions and numbers as single tokens"],
"tags": ["tokenization", "normalization", "regex", "unicode"],
"sources": ["S017", "S018"], "entry": "normalize(text); tokenize(text)",
"article": r'''
# Normalisation and Tokenisation

## Intuition
Computers see "Café", "cafe" and "CAFÉ" as three different strings. Before counting words we
normalise text and split it into **tokens** — the units a model will count or embed.

## Precise explanation
**Normalisation** (one common recipe):
1. `unicodedata.normalize("NFKD", s)` decomposes "é" into "e" + a combining accent mark.
2. Drop combining marks (`unicodedata.combining(ch)` is non-zero for them).
3. Lowercase.
This is a design choice: it helps search in English but destroys meaning in languages where
accents matter.

**Tokenisation with a regex:** `re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)` returns runs of letters
and digits, optionally followed by an apostrophe part ("don't", "it's"). Everything else
(spaces, punctuation) separates tokens.

Real tokenisers (NLTK, spaCy, subword BPE in [[bpe-merges]]) make many more decisions; the point is that
tokenisation is a modelling choice with consequences.

## Worked example
"Café's menu: 2 croissants, NO coffee!" → normalise → "cafe's menu: 2 croissants, no coffee!" →
tokens [cafe's, menu, 2, croissants, no, coffee].

## Common mistakes
* `text.split()` keeps punctuation attached ("coffee!").
* Forgetting to normalise before tokenising, so accented letters are dropped by `[a-z]`.
* Using `\w`, which also matches underscores and non-Latin letters (sometimes desired, sometimes not).

## Why this matters
Every later NLP and LLM exercise starts from tokens; inconsistent tokenisation between training
and inference silently hurts models.
''',
"statement": r'''
Implement:
* `normalize(text)` → NFKD-decompose, remove combining characters, lowercase.
* `tokenize(text)` → `re.findall(r"[a-z0-9]+(?:'[a-z]+)?", normalize(text))`.

**Examples**
```python
normalize("Café ÉLAN")   # 'cafe elan'
tokenize("Café's menu: 2 croissants, NO coffee!")
# ["cafe's", 'menu', '2', 'croissants', 'no', 'coffee']
tokenize("--- ...")      # []
```
''',
"starter": r'''
import re
import unicodedata


def normalize(text):
    # TODO
    pass


def tokenize(text):
    # TODO
    return []
''',
"hints": [
    "`unicodedata.normalize('NFKD', text)`.",
    "`''.join(ch for ch in s if not unicodedata.combining(ch)).lower()`.",
    "Apply the given regex with `re.findall` to the normalised text.",
],
"solution": r'''
import re
import unicodedata

TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def normalize(text):
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).lower()


def tokenize(text):
    return TOKEN_RE.findall(normalize(text))
''',
"explanation": r'''
NFKD splits accented letters into base letters plus combining marks, which are then removed.
Lowercasing finishes normalisation. A compiled regex extracts alphanumeric runs with an optional
apostrophe suffix, so contractions remain one token.
''',
"tests": r'''
class TestTokenize(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(S.normalize("Café ÉLAN"), "cafe elan")

    def test_tokens(self):
        self.assertEqual(S.tokenize("Café's menu: 2 croissants, NO coffee!"),
                         ["cafe's", "menu", "2", "croissants", "no", "coffee"])

    def test_empty_and_punct(self):
        self.assertEqual(S.tokenize(""), [])
        self.assertEqual(S.tokenize("--- ..."), [])

    def test_contraction(self):
        self.assertEqual(S.tokenize("I don't know, it's fine."), ["i", "don't", "know", "it's", "fine"])

    def test_numbers(self):
        self.assertEqual(S.tokenize("Version 3.11 in 2026"), ["version", "3", "11", "in", "2026"])

    def test_whitespace_variants(self):
        self.assertEqual(S.tokenize("a\tb\nc  d"), ["a", "b", "c", "d"])

    def test_accent_mid_word(self):
        self.assertEqual(S.tokenize("naïve résumé"), ["naive", "resume"])
''',
"feedback": [
    ("test_normalize", "Use NFKD and drop characters where unicodedata.combining(ch) is non-zero."),
    ("test_tokens", "Normalise before applying the lowercase regex."),
    ("test_contraction", "Keep the optional (?:'[a-z]+) group in the regex."),
    ("test_accent_mid_word", "Accented letters must become plain letters, not separators."),
],
},
# ---------------------------------------------------------------- stopword-counts
{
"slug": "stopword-counts", "title": "Stopwords and Word Counts", "optional": True,
"difficulty": "beginner", "prereqs": ["tokenize-normalize"], "packages": [],
"objectives": ["Remove stopwords", "Count tokens with collections.Counter",
               "Return top-n words with deterministic tie-breaking"],
"tags": ["stopwords", "word-frequency", "counter"],
"sources": ["S018", "S017"], "entry": "remove_stopwords(tokens, stopwords); top_words(tokens, n, stopwords=())",
"article": r'''
# Stopwords and Frequencies

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
''',
"statement": r'''
Implement:
* `remove_stopwords(tokens, stopwords)` → new list without stopwords (order kept).
* `top_words(tokens, n, stopwords=())` → list of `(word, count)` for the `n` most frequent
  non-stopwords, sorted by count descending then word ascending. Raise `ValueError` if `n < 1`.

**Example**
```python
toks = ["the", "cat", "and", "the", "hat", "cat", "sat"]
remove_stopwords(toks, {"the", "and"})   # ['cat', 'hat', 'cat', 'sat']
top_words(toks, 2, {"the", "and"})       # [('cat', 2), ('hat', 1)]
```
''',
"starter": r'''
from collections import Counter


def remove_stopwords(tokens, stopwords):
    # TODO
    return []


def top_words(tokens, n, stopwords=()):
    # TODO
    return []
''',
"hints": [
    "Convert stopwords to a set once: `sw = set(stopwords)`.",
    "`Counter(remove_stopwords(tokens, stopwords))`.",
    "`sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]`.",
],
"solution": r'''
from collections import Counter


def remove_stopwords(tokens, stopwords):
    sw = set(stopwords)
    return [t for t in tokens if t not in sw]


def top_words(tokens, n, stopwords=()):
    if n < 1:
        raise ValueError("n must be >= 1")
    counts = Counter(remove_stopwords(tokens, stopwords))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
''',
"explanation": r'''
A set makes stopword checks constant time. `Counter` tallies the remaining tokens and an explicit
sort key gives a stable, deterministic ranking independent of token order.
''',
"tests": r'''
TOKS = ["the", "cat", "and", "the", "hat", "cat", "sat"]

class TestCounts(unittest.TestCase):
    def test_remove(self):
        self.assertEqual(S.remove_stopwords(TOKS, {"the", "and"}), ["cat", "hat", "cat", "sat"])

    def test_top(self):
        self.assertEqual(S.top_words(TOKS, 2, {"the", "and"}), [("cat", 2), ("hat", 1)])

    def test_no_stopwords(self):
        self.assertEqual(S.top_words(TOKS, 1), [("cat", 2)])
        self.assertEqual(S.top_words(TOKS, 2), [("cat", 2), ("the", 2)])

    def test_n_larger(self):
        self.assertEqual(len(S.top_words(["a", "b"], 10)), 2)

    def test_empty(self):
        self.assertEqual(S.top_words([], 3), [])

    def test_bad_n(self):
        with self.assertRaises(ValueError):
            S.top_words(TOKS, 0)

    def test_order_independent(self):
        self.assertEqual(S.top_words(["b", "a", "b", "a"], 2), [("a", 2), ("b", 2)])
''',
"feedback": [
    ("test_top", "Sort by (-count, word) so ties are alphabetical."),
    ("test_order_independent", "Counter.most_common keeps insertion order on ties — sort explicitly."),
    ("test_remove", "Keep the original order of non-stopwords."),
    ("test_bad_n", "Raise ValueError when n < 1."),
],
},
# ---------------------------------------------------------------- bag-of-words
{
"slug": "bag-of-words", "title": "Bag-of-Words Vectors",
"difficulty": "intermediate", "prereqs": ["nlp-countvectorizer"], "packages": ["numpy"],
"objectives": ["Build a vocabulary with a minimum count", "Map documents to count vectors",
               "Handle out-of-vocabulary tokens"],
"tags": ["bag-of-words", "vocabulary", "vectorization", "oov"],
"sources": ["S017", "S012"], "entry": "build_vocab(docs, min_count=1); vectorize(docs, vocab)",
"article": r'''
# Bag of Words

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
Bag-of-words feeds TF-IDF ([[tf-idf]]), Naive Bayes ([[naive-bayes-text]]) and is the baseline any neural text model
should beat.
''',
"statement": r'''
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
''',
"starter": r'''
from collections import Counter

import numpy as np


def build_vocab(docs, min_count=1):
    # TODO
    return {}


def vectorize(docs, vocab):
    # TODO
    pass
''',
"hints": [
    "`c = Counter(t for doc in docs for t in doc)`.",
    "`words = sorted(w for w, k in c.items() if k >= min_count)`; enumerate them.",
    "Loop documents and tokens; `if t in vocab: X[i, vocab[t]] += 1`.",
],
"solution": r'''
from collections import Counter

import numpy as np


def build_vocab(docs, min_count=1):
    c = Counter(t for doc in docs for t in doc)
    words = sorted(w for w, k in c.items() if k >= min_count)
    return {w: i for i, w in enumerate(words)}


def vectorize(docs, vocab):
    X = np.zeros((len(docs), len(vocab)), dtype=int)
    for i, doc in enumerate(docs):
        for t in doc:
            j = vocab.get(t)
            if j is not None:
                X[i, j] += 1
    return X
''',
"explanation": r'''
Counting all tokens once gives total frequencies for the `min_count` filter; sorting fixes the
column order. Vectorisation looks each token up and increments its column, skipping OOV words.
''',
"tests": r'''
import numpy as np

DOCS = [["a", "b", "a"], ["b", "c"]]

class TestBoW(unittest.TestCase):
    def test_vocab(self):
        self.assertEqual(S.build_vocab(DOCS), {"a": 0, "b": 1, "c": 2})

    def test_vectors(self):
        np.testing.assert_array_equal(S.vectorize(DOCS, S.build_vocab(DOCS)), [[2, 1, 0], [0, 1, 1]])

    def test_min_count(self):
        self.assertEqual(S.build_vocab(DOCS, min_count=2), {"a": 0, "b": 1})

    def test_oov(self):
        X = S.vectorize([["z", "a"]], S.build_vocab(DOCS))
        np.testing.assert_array_equal(X, [[1, 0, 0]])

    def test_empty_doc(self):
        X = S.vectorize([[]], S.build_vocab(DOCS))
        self.assertEqual(X.shape, (1, 3))
        self.assertEqual(X.sum(), 0)

    def test_alphabetical(self):
        self.assertEqual(list(S.build_vocab([["zeta", "alpha", "mid"]])), ["alpha", "mid", "zeta"])

    def test_row_sums(self):
        docs = [["x", "y", "x", "x"], ["y"]]
        np.testing.assert_array_equal(S.vectorize(docs, S.build_vocab(docs)).sum(axis=1), [4, 1])
''',
"feedback": [
    ("test_vocab", "Assign indices in alphabetical order."),
    ("test_min_count", "Filter by total count across all documents."),
    ("test_oov", "Ignore tokens not in the vocabulary instead of raising KeyError."),
    ("test_vectors", "Increment X[i, vocab[t]] for every token."),
],
},
# ---------------------------------------------------------------- char-ngrams
{
"slug": "char-ngrams", "title": "Character n-grams by Hand", "optional": True,
"difficulty": "beginner", "prereqs": ["tokenize-normalize"], "packages": [],
"objectives": ["Extract character n-grams with boundary markers", "Generate ranges of n",
               "Compare words by n-gram overlap (Jaccard)"],
"tags": ["char-ngrams", "subwords", "jaccard"],
"sources": ["S017", "S020"], "entry": "char_ngrams(word, n_min=3, n_max=3); jaccard(a, b, n=3)",
"article": r'''
# Character n-grams

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
Character and subword units (BPE, [[bpe-merges]]) are how modern language models avoid out-of-vocabulary
words.
''',
"statement": r'''
Implement:
* `char_ngrams(word, n_min=3, n_max=3)` → list of n-grams of `"<"+word+">"`, ordered by n
  ascending then by position. Raise `ValueError` if `n_min < 1` or `n_max < n_min`.
* `jaccard(a, b, n=3)` → Jaccard similarity of the *sets* of n-grams of words `a` and `b`
  (1.0 if both sets are empty).

**Examples**
```python
char_ngrams("cat")             # ['<ca', 'cat', 'at>']
char_ngrams("ab", 2, 3)        # ['<a', 'ab', 'b>', '<ab', 'ab>']
jaccard("cat", "cart")         # 0.16666...
```
''',
"starter": r'''
def char_ngrams(word, n_min=3, n_max=3):
    # TODO
    return []


def jaccard(a, b, n=3):
    # TODO
    pass
''',
"hints": [
    "`s = '<' + word + '>'`.",
    "For each n in range(n_min, n_max + 1): `[s[i:i+n] for i in range(len(s) - n + 1)]`.",
    "Sets: `A = set(char_ngrams(a, n, n))`; return `len(A & B) / len(A | B)`.",
],
"solution": r'''
def char_ngrams(word, n_min=3, n_max=3):
    if n_min < 1 or n_max < n_min:
        raise ValueError("need 1 <= n_min <= n_max")
    s = "<" + word + ">"
    out = []
    for n in range(n_min, n_max + 1):
        out.extend(s[i:i + n] for i in range(len(s) - n + 1))
    return out


def jaccard(a, b, n=3):
    A, B = set(char_ngrams(a, n, n)), set(char_ngrams(b, n, n))
    union = A | B
    return 1.0 if not union else len(A & B) / len(union)
''',
"explanation": r'''
Markers are added once; each n contributes all windows of that length in order. Jaccard compares
n-gram sets, handling the empty case explicitly.
''',
"tests": r'''
class TestCharNgrams(unittest.TestCase):
    def test_cat(self):
        self.assertEqual(S.char_ngrams("cat"), ["<ca", "cat", "at>"])

    def test_range(self):
        self.assertEqual(S.char_ngrams("ab", 2, 3), ["<a", "ab", "b>", "<ab", "ab>"])

    def test_short_word(self):
        self.assertEqual(S.char_ngrams("a", 4, 4), [])
        self.assertEqual(S.char_ngrams("", 2, 2), ["<>"])

    def test_count(self):
        self.assertEqual(len(S.char_ngrams("banana", 3, 3)), len("<banana>") - 2)

    def test_jaccard(self):
        self.assertAlmostEqual(S.jaccard("cat", "cart"), 1 / 6)
        self.assertEqual(S.jaccard("same", "same"), 1.0)

    def test_jaccard_disjoint_and_empty(self):
        self.assertEqual(S.jaccard("abc", "xyz"), 0.0)
        self.assertEqual(S.jaccard("a", "b", n=5), 1.0)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.char_ngrams("x", 3, 2)
''',
"feedback": [
    ("test_cat", "Wrap the word in '<' and '>' before slicing."),
    ("test_range", "Order by n first, then by position."),
    ("test_jaccard", "Use sets of n-grams: |A ∩ B| / |A ∪ B|."),
    ("test_jaccard_disjoint_and_empty", "Return 1.0 when both n-gram sets are empty."),
],
},
# ---------------------------------------------------------------- bigram-counts
{
"slug": "bigram-counts", "title": "Bigram Counts with Sentence Markers", "optional": True,
"difficulty": "intermediate", "prereqs": ["stopword-counts"], "packages": [],
"objectives": ["Pad sentences with <s> and </s>", "Count bigrams and unigram contexts",
               "Estimate maximum-likelihood bigram probabilities"],
"tags": ["n-grams", "bigrams", "language-models", "mle"],
"sources": ["S017", "S018"], "entry": "bigram_counts(sentences); bigram_prob(w_prev, w, counts)",
"article": r'''
# Bigram Counts

## Intuition
To guess the next word, look at what usually follows the current one. After "of", "the" is
common; after "the", a noun. Counting adjacent word pairs (bigrams) captures this.

## Precise explanation
Pad each sentence with a start marker `<s>` and an end marker `</s>`:
`<s> i like tea </s>`. Bigrams are consecutive pairs: (`<s>`, i), (i, like), (like, tea),
(tea, `</s>`). The maximum-likelihood estimate is
$$P(w \mid w_\text{prev}) = \frac{C(w_\text{prev}, w)}{C(w_\text{prev}\ \text{as a context})},$$
where the denominator counts how often $w_\text{prev}$ appears as the **first** element of a
bigram. (`</s>` is never a context.) Unseen contexts have undefined probability — [[bigram-next-token]] adds
smoothing.

## Worked example
Sentences "i like tea", "i like coffee": C(i, like) = 2, C(like, tea) = 1, contexts: like = 2 →
P(tea | like) = 0.5, P(like | `<s>`)… P(i | `<s>`) = 1.

## Common mistakes
* Counting bigrams across sentence boundaries.
* Using total unigram counts (including the final position) as the denominator.
* Forgetting the markers, losing "which words start sentences".

## Why this matters
N-gram models are the ancestors of LLMs: both predict the next token from context. Their
weaknesses (sparsity, short context) motivate neural models.
''',
"statement": r'''
Implement:
* `bigram_counts(sentences)` → dict with `"bigrams"` (`Counter` of `(prev, word)` tuples) and
  `"contexts"` (`Counter` of how often each token is the first element of a bigram). Each sentence
  is a token list padded with `<s>` and `</s>`.
* `bigram_prob(w_prev, w, counts)` → MLE probability; raise `KeyError` if `w_prev` was never a
  context.

**Example**
```python
c = bigram_counts([["i", "like", "tea"], ["i", "like", "coffee"]])
c["bigrams"][("i", "like")]        # 2
bigram_prob("like", "tea", c)      # 0.5
bigram_prob("<s>", "i", c)         # 1.0
```
''',
"starter": r'''
from collections import Counter


def bigram_counts(sentences):
    # TODO
    return {"bigrams": Counter(), "contexts": Counter()}


def bigram_prob(w_prev, w, counts):
    # TODO
    pass
''',
"hints": [
    "`toks = ['<s>'] + sent + ['</s>']`.",
    "`for a, b in zip(toks, toks[1:]): bigrams[(a, b)] += 1; contexts[a] += 1`.",
    "`counts['bigrams'][(w_prev, w)] / counts['contexts'][w_prev]`.",
],
"solution": r'''
from collections import Counter


def bigram_counts(sentences):
    bigrams, contexts = Counter(), Counter()
    for sent in sentences:
        toks = ["<s>"] + list(sent) + ["</s>"]
        for a, b in zip(toks, toks[1:]):
            bigrams[(a, b)] += 1
            contexts[a] += 1
    return {"bigrams": bigrams, "contexts": contexts}


def bigram_prob(w_prev, w, counts):
    ctx = counts["contexts"].get(w_prev, 0)
    if ctx == 0:
        raise KeyError(w_prev)
    return counts["bigrams"].get((w_prev, w), 0) / ctx
''',
"explanation": r'''
Each padded sentence contributes its consecutive pairs; the first token of every pair is also
counted as a context. The MLE probability divides the pair count by the context count, so
probabilities for a context sum to one.
''',
"tests": r'''
SENTS = [["i", "like", "tea"], ["i", "like", "coffee"]]

class TestBigrams(unittest.TestCase):
    def test_counts(self):
        c = S.bigram_counts(SENTS)
        self.assertEqual(c["bigrams"][("i", "like")], 2)
        self.assertEqual(c["bigrams"][("tea", "</s>")], 1)
        self.assertEqual(c["contexts"]["<s>"], 2)

    def test_prob(self):
        c = S.bigram_counts(SENTS)
        self.assertEqual(S.bigram_prob("like", "tea", c), 0.5)
        self.assertEqual(S.bigram_prob("<s>", "i", c), 1.0)

    def test_unseen_pair(self):
        self.assertEqual(S.bigram_prob("i", "tea", S.bigram_counts(SENTS)), 0.0)

    def test_unknown_context(self):
        with self.assertRaises(KeyError):
            S.bigram_prob("</s>", "i", S.bigram_counts(SENTS))

    def test_no_cross_sentence(self):
        self.assertEqual(S.bigram_counts(SENTS)["bigrams"][("tea", "i")], 0)

    def test_sums_to_one(self):
        c = S.bigram_counts([["a", "b", "a", "c"], ["a", "a"]])
        vocab = {w for pair in c["bigrams"] for w in pair}
        for ctx in c["contexts"]:
            self.assertAlmostEqual(sum(S.bigram_prob(ctx, w, c) for w in vocab), 1.0)

    def test_empty_sentence(self):
        c = S.bigram_counts([[]])
        self.assertEqual(c["bigrams"][("<s>", "</s>")], 1)
''',
"feedback": [
    ("test_counts", "Pad every sentence with <s> and </s> before pairing."),
    ("test_no_cross_sentence", "Count pairs within each sentence only."),
    ("test_unknown_context", "Raise KeyError when the context was never seen."),
    ("test_sums_to_one", "Divide by context counts (first element of bigrams), not all unigram counts."),
],
},
# ---------------------------------------------------------------- tf-idf
{
"slug": "tf-idf", "title": "TF-IDF",
"difficulty": "intermediate", "prereqs": ["bag-of-words"], "packages": ["numpy"],
"objectives": ["Compute document frequency and smoothed IDF", "Weight term frequencies by IDF",
               "L2-normalise document vectors"],
"tags": ["tf-idf", "information-retrieval", "weighting", "normalisation"],
"sources": ["S017", "S012"], "entry": "tfidf(counts)",
"article": r'''
# TF-IDF

## Intuition
A word matters for a document if it appears there often (term frequency) but is rare across the
collection (inverse document frequency). "the" is frequent everywhere — low weight; "photosynthesis"
in one biology document — high weight.

## Precise explanation
Given a count matrix $C$ `(n_docs, n_terms)` ([[bag-of-words]]):
* document frequency $\text{df}_t$ = number of documents with $C_{dt} > 0$;
* smoothed IDF (the scikit-learn default `smooth_idf=True`):
  $\text{idf}_t = \ln\frac{1 + n}{1 + \text{df}_t} + 1$;
* weights $W_{dt} = C_{dt}\cdot \text{idf}_t$ (raw counts as TF);
* L2-normalise each row: $W_d / \lVert W_d\rVert_2$ (rows of all zeros stay zero).
The "+1"s avoid division by zero and keep terms that appear in every document from getting
weight exactly 0.

## Worked example
2 docs, terms [a, b]: C = [[1, 1], [2, 0]]. df = [2, 1]; idf = [ln(3/3)+1, ln(3/2)+1] =
[1, 1.405]. Row 0: [1, 1.405] / 1.725 = [0.580, 0.815]; row 1: [2, 0] → [1, 0].

## Common mistakes
* Using log base 10 vs natural log inconsistently.
* Normalising columns instead of rows.
* Dividing by zero for empty documents.

## Why this matters
TF-IDF is a strong baseline for search and classification and the "sparse" half of modern
hybrid retrieval in RAG systems.
''',
"statement": r'''
Write `tfidf(counts)` for an integer count matrix (NumPy array, `(n_docs, n_terms)`) returning
`(W, idf)`: the L2-row-normalised TF-IDF matrix (floats) and the IDF vector, using the smoothed
formula above with natural logs. Raise `ValueError` for negative counts or non-2-D input.

**Example**
```python
W, idf = tfidf(np.array([[1, 1], [2, 0]]))
idf    # [1.        , 1.40546511]
W      # [[0.57973867, 0.81480247], [1., 0.]]
```
''',
"starter": r'''
import numpy as np


def tfidf(counts):
    # TODO
    pass
''',
"hints": [
    "`df = (C > 0).sum(axis=0)`; `n = C.shape[0]`.",
    "`idf = np.log((1 + n) / (1 + df)) + 1`; `W = C * idf`.",
    "`norms = np.linalg.norm(W, axis=1, keepdims=True)`; divide where norms > 0.",
],
"solution": r'''
import numpy as np


def tfidf(counts):
    C = np.asarray(counts, dtype=float)
    if C.ndim != 2 or (C < 0).any():
        raise ValueError("counts must be a non-negative 2-D array")
    n = C.shape[0]
    df = (C > 0).sum(axis=0)
    idf = np.log((1 + n) / (1 + df)) + 1.0
    W = C * idf
    norms = np.linalg.norm(W, axis=1, keepdims=True)
    W = np.divide(W, norms, out=np.zeros_like(W), where=norms > 0)
    return W, idf
''',
"explanation": r'''
Document frequency counts non-zero entries per column; smoothed IDF follows. Broadcasting
multiplies each column by its IDF, and rows are scaled to unit length, with empty rows left as
zeros via a guarded division.
''',
"tests": r'''
import numpy as np

class TestTFIDF(unittest.TestCase):
    def test_example(self):
        W, idf = S.tfidf(np.array([[1, 1], [2, 0]]))
        np.testing.assert_allclose(idf, [1.0, np.log(1.5) + 1])
        np.testing.assert_allclose(W, [[1 / np.hypot(1, idf[1]), idf[1] / np.hypot(1, idf[1])], [1, 0]])

    def test_unit_rows(self):
        W, _ = S.tfidf(np.array([[3, 0, 1], [0, 2, 2], [1, 1, 1]]))
        np.testing.assert_allclose(np.linalg.norm(W, axis=1), 1.0)

    def test_empty_doc(self):
        W, _ = S.tfidf(np.array([[0, 0], [1, 0]]))
        np.testing.assert_array_equal(W[0], [0, 0])

    def test_common_term_lower_weight(self):
        W, idf = S.tfidf(np.array([[1, 1], [1, 0], [1, 0]]))
        self.assertGreater(idf[1], idf[0])
        self.assertGreater(W[0, 1], W[0, 0])

    def test_idf_formula(self):
        _, idf = S.tfidf(np.array([[1, 0, 0], [1, 1, 0], [1, 1, 0], [0, 0, 1]]))
        np.testing.assert_allclose(idf, np.log(5 / (1 + np.array([3, 2, 1]))) + 1)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.tfidf(np.array([[-1, 2]]))
''',
"feedback": [
    ("test_idf_formula", "idf = ln((1 + n)/(1 + df)) + 1 with natural log."),
    ("test_unit_rows", "Normalise each row (axis=1) to unit L2 norm."),
    ("test_empty_doc", "Guard the division so empty documents stay all-zero."),
    ("test_example", "Multiply raw counts by idf before normalising."),
],
},
# ---------------------------------------------------------------- cosine-retrieval
{
"slug": "cosine-retrieval", "title": "Cosine Similarity Retrieval", "optional": True,
"difficulty": "intermediate", "prereqs": ["tf-idf"], "packages": ["numpy"],
"objectives": ["Compute cosine similarity between query and documents", "Rank documents with stable top-k",
               "Handle zero vectors"],
"tags": ["cosine-similarity", "retrieval", "ranking", "search"],
"sources": ["S017", "S007"], "entry": "cosine_matrix(A, B); search(query_vec, doc_matrix, k)",
"article": r'''
# Retrieval with Cosine Similarity

## Intuition
Two documents about the same topic use similar words in similar *proportions*, even if one is
much longer. Cosine similarity compares directions, ignoring length.

## Precise explanation
$$\cos(a, b) = \frac{a\cdot b}{\lVert a\rVert\,\lVert b\rVert}\in[-1, 1]$$
(in [0, 1] for non-negative TF-IDF vectors). For matrices with rows as vectors:
normalise rows, then `A_n @ B_n.T` gives all pairwise cosines. A zero vector has no direction;
define its cosine with anything as 0.
**Search:** score every document against the query and return the top k indices (stable order on
ties, [[fancy-indexing]]).

## Worked example
q = [1, 1, 0], docs [[2, 2, 0], [0, 0, 5], [1, 0, 0]] → cosines [1, 0, 0.707] → ranking [0, 2, 1].

## Common mistakes
* Dot products without normalisation (long documents always win).
* NaN from 0/0 for empty vectors.
* Reversing argsort and breaking tie order.

## Why this matters
This is the retrieval step in search engines and retrieval-augmented generation (with dense
embeddings instead of TF-IDF).
''',
"statement": r'''
Implement:
* `cosine_matrix(A, B)` → `(len(A), len(B))` cosines between rows (0 where a row is all zeros).
* `search(query_vec, doc_matrix, k)` → list of `(doc_index, score)` for the `k` best documents,
  highest score first, ties by lower index. Raise `ValueError` unless `1 <= k <= n_docs`.

**Example**
```python
search(np.array([1., 1., 0.]), np.array([[2., 2., 0.], [0., 0., 5.], [1., 0., 0.]]), 2)
# [(0, 1.0), (2, 0.7071...)]
```
''',
"starter": r'''
import numpy as np


def cosine_matrix(A, B):
    # TODO
    pass


def search(query_vec, doc_matrix, k):
    # TODO
    return []
''',
"hints": [
    "Row-normalise with a guarded division: zero rows stay zero.",
    "`An @ Bn.T` gives all cosines.",
    "`order = np.argsort(-scores, kind='stable')[:k]`.",
],
"solution": r'''
import numpy as np


def _normalise_rows(M):
    M = np.asarray(M, dtype=float)
    n = np.linalg.norm(M, axis=1, keepdims=True)
    return np.divide(M, n, out=np.zeros_like(M), where=n > 0)


def cosine_matrix(A, B):
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    if A.shape[1] != B.shape[1]:
        raise ValueError("dimension mismatch")
    return _normalise_rows(A) @ _normalise_rows(B).T


def search(query_vec, doc_matrix, k):
    D = np.atleast_2d(doc_matrix)
    if not 1 <= k <= D.shape[0]:
        raise ValueError("k out of range")
    scores = cosine_matrix(np.atleast_2d(query_vec), D)[0]
    order = np.argsort(-scores, kind="stable")[:k]
    return [(int(i), float(scores[i])) for i in order]
''',
"explanation": r'''
Normalising rows turns dot products into cosines; zero rows remain zero so their cosines are 0.
The query's scores against all documents are ranked with a stable descending sort.
''',
"tests": r'''
import numpy as np

D = np.array([[2., 2., 0.], [0., 0., 5.], [1., 0., 0.]])

class TestRetrieval(unittest.TestCase):
    def test_search(self):
        r = S.search(np.array([1., 1., 0.]), D, 2)
        self.assertEqual([i for i, _ in r], [0, 2])
        self.assertAlmostEqual(r[0][1], 1.0)
        self.assertAlmostEqual(r[1][1], 1 / np.sqrt(2))

    def test_matrix(self):
        C = S.cosine_matrix(D, D)
        np.testing.assert_allclose(np.diag(C), 1.0)
        self.assertAlmostEqual(C[0, 1], 0.0)

    def test_zero_vector(self):
        C = S.cosine_matrix(np.zeros((1, 3)), D)
        np.testing.assert_array_equal(C, [[0, 0, 0]])

    def test_length_invariance(self):
        a = S.cosine_matrix(np.array([[1., 2., 3.]]), np.array([[2., 4., 6.]]))
        self.assertAlmostEqual(a[0, 0], 1.0)

    def test_ties_stable(self):
        r = S.search(np.array([1., 0.]), np.array([[1., 0.], [3., 0.], [0., 1.]]), 3)
        self.assertEqual([i for i, _ in r], [0, 1, 2])

    def test_bad_k(self):
        with self.assertRaises(ValueError):
            S.search(np.array([1., 0., 0.]), D, 4)
''',
"feedback": [
    ("test_search", "Normalise rows before taking dot products."),
    ("test_zero_vector", "Zero vectors must give cosine 0, not NaN."),
    ("test_ties_stable", "Use np.argsort(-scores, kind='stable')."),
    ("test_bad_k", "Validate 1 <= k <= number of documents."),
],
},
# ---------------------------------------------------------------- levenshtein
{
"slug": "levenshtein", "title": "Levenshtein Edit Distance",
"difficulty": "intermediate", "prereqs": ["nlp-char-ngrams-sklearn"], "packages": [],
"objectives": ["Fill a dynamic-programming table", "Compute minimum insert/delete/substitute edits",
               "Build a simple spelling suggester"],
"tags": ["edit-distance", "dynamic-programming", "spelling-correction"],
"sources": ["S017"], "entry": "levenshtein(a, b); suggest(word, vocab, max_dist=2)",
"article": r'''
# Edit Distance

## Intuition
How many single-character edits turn "kitten" into "sitting"? Substitute k→s, substitute e→i,
insert g: three. The smallest such number is the **Levenshtein distance**.

## Precise explanation
Let $D[i][j]$ be the distance between the first $i$ characters of $a$ and the first $j$ of $b$:
$$D[i][0] = i,\quad D[0][j] = j,$$
$$D[i][j] = \min\big(D[i-1][j] + 1,\ D[i][j-1] + 1,\ D[i-1][j-1] + [a_i \ne b_j]\big).$$
(deletion, insertion, substitution/match). The answer is $D[|a|][|b|]$. Time $O(|a||b|)$; only
two rows are needed for memory $O(|b|)$.

| | "" | s | i | t |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| k | 1 | 1 | 2 | 3 |
| i | 2 | 2 | 1 | 2 |
| t | 3 | 3 | 2 | 1 |

*Table: D for "kit" → "sit": distance 1.*

## Worked example
levenshtein("kitten", "sitting") = 3; levenshtein("", "abc") = 3.

## Common mistakes
* Forgetting the first row/column initialisation.
* Off-by-one between string index and table index (`a[i-1]`).
* Exponential recursion without memoisation.

## Why this matters
Edit distance powers spelling correction, fuzzy matching and evaluation metrics such as word error
rate in speech recognition.
''',
"statement": r'''
Implement:
* `levenshtein(a, b)` → int, using DP (insert, delete, substitute all cost 1).
* `suggest(word, vocab, max_dist=2)` → list of vocabulary words with distance `<= max_dist`,
  sorted by distance then alphabetically.

**Examples**
```python
levenshtein("kitten", "sitting")   # 3
levenshtein("", "abc")             # 3
suggest("teh", ["the", "tea", "ten", "apple"], 2)   # ['tea', 'ten', 'the']
```
''',
"starter": r'''
def levenshtein(a, b):
    # TODO
    pass


def suggest(word, vocab, max_dist=2):
    # TODO
    return []
''',
"hints": [
    "`prev = list(range(len(b) + 1))` is row 0.",
    "For each i: `cur = [i]`; append `min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (a[i-1] != b[j-1]))`.",
    "`sorted((levenshtein(word, w), w) for w in vocab)` then filter by max_dist.",
],
"solution": r'''
def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i]
        for j in range(1, len(b) + 1):
            cur.append(min(prev[j] + 1,
                           cur[j - 1] + 1,
                           prev[j - 1] + (a[i - 1] != b[j - 1])))
        prev = cur
    return prev[-1]


def suggest(word, vocab, max_dist=2):
    scored = sorted((levenshtein(word, w), w) for w in set(vocab))
    return [w for d, w in scored if d <= max_dist]
''',
"explanation": r'''
The table is filled row by row keeping only the previous row. Each cell takes the cheapest of
deletion, insertion and substitution (free when characters match). Suggestions sort
(distance, word) pairs for a deterministic ranking.
''',
"tests": r'''
class TestLev(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(S.levenshtein("kitten", "sitting"), 3)

    def test_empty(self):
        self.assertEqual(S.levenshtein("", "abc"), 3)
        self.assertEqual(S.levenshtein("", ""), 0)

    def test_symmetric(self):
        self.assertEqual(S.levenshtein("flaw", "lawn"), S.levenshtein("lawn", "flaw"))
        self.assertEqual(S.levenshtein("flaw", "lawn"), 2)

    def test_identical(self):
        self.assertEqual(S.levenshtein("same", "same"), 0)

    def test_suggest(self):
        self.assertEqual(S.suggest("teh", ["the", "tea", "ten", "apple"], 2), ["tea", "ten", "the"])

    def test_suggest_ordering(self):
        self.assertEqual(S.suggest("cat", ["cart", "cat", "act", "dog"], 2), ["cat", "cart", "act"])

    def test_triangle(self):
        a, b, c = "intention", "execution", "extension"
        self.assertLessEqual(S.levenshtein(a, c), S.levenshtein(a, b) + S.levenshtein(b, c))
        self.assertEqual(S.levenshtein(a, b), 5)
''',
"feedback": [
    ("test_classic", "Substitution cost is 0 when characters match, else 1."),
    ("test_empty", "Initialise row 0 as 0..len(b) and column 0 as i."),
    ("test_suggest_ordering", "Sort by (distance, word)."),
    ("test_triangle", "intention→execution is the textbook example with distance 5."),
],
},
# ---------------------------------------------------------------- naive-bayes-text
{
"slug": "naive-bayes-text", "title": "Multinomial Naive Bayes Text Classifier",
"difficulty": "advanced", "prereqs": ["bag-of-words", "conditional-bayes"], "packages": ["numpy"],
"objectives": ["Estimate class priors and per-class word probabilities with Laplace smoothing",
               "Classify in log space", "Explain the conditional-independence assumption"],
"tags": ["naive-bayes", "text-classification", "laplace-smoothing", "log-probabilities"],
"sources": ["S017", "S012"], "entry": "class MultinomialNB(alpha=1.0): fit(X, y), predict_log_proba(X), predict(X)",
"article": r'''
# Multinomial Naive Bayes

## Intuition
Spam emails use words like "free" and "winner" more often. Naive Bayes estimates, for each class,
how likely each word is, then asks which class makes the observed words most probable — assuming
(naively) that words occur independently given the class.

## Precise explanation
For count vectors $x$ (bag of words) and classes $c$:
$$\log P(c\mid x) = \log P(c) + \sum_t x_t \log \theta_{ct} - \log Z,$$
with priors $P(c) = n_c / n$ and **Laplace (add-α) smoothing**
$$\theta_{ct} = \frac{N_{ct} + \alpha}{\sum_{t'} N_{ct'} + \alpha V},$$
where $N_{ct}$ is the total count of term t in class c documents and V the vocabulary size.
Smoothing prevents a single unseen word from making a probability exactly zero. Work in **log
space** (sums instead of products) to avoid underflow; normalise with log-sum-exp.

## Worked example
Class spam: counts [free: 3, meet: 0]; ham: [free: 0, meet: 2]; α = 1, V = 2:
θ_spam = [4/5, 1/5], θ_ham = [1/4, 3/4]. A document "free" favours spam.

## Common mistakes
* No smoothing → log(0) = −inf.
* Multiplying many small probabilities (underflow).
* Using document frequency instead of term counts.

## Why this matters
Naive Bayes is a fast, surprisingly strong baseline for text classification and a clear example of
generative classification.
''',
"statement": r'''
Implement `class MultinomialNB(alpha=1.0)` for an integer count matrix `X` `(n, V)` and labels
`y` (any hashable class values):
* `fit(X, y)` → stores `classes_` (sorted unique labels), `class_log_prior_` `(K,)` and
  `feature_log_prob_` `(K, V)`; returns `self`. Raise `ValueError` if `alpha <= 0`.
* `predict_log_proba(X)` → `(n, K)` normalised log posteriors (rows log-sum-exp to 0).
* `predict(X)` → array of class labels (argmax; ties → first class in `classes_`).

**Example**
```python
X = np.array([[3, 0], [0, 2]]); y = np.array(["spam", "ham"])
m = MultinomialNB().fit(X, y)
np.exp(m.feature_log_prob_)      # [[0.25, 0.75], [0.8, 0.2]]   (classes_ = ['ham', 'spam'])
m.predict(np.array([[1, 0]]))    # ['spam']
```
''',
"starter": r'''
import numpy as np


class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        # TODO
        return self

    def predict_log_proba(self, X):
        # TODO
        pass

    def predict(self, X):
        # TODO
        pass
''',
"hints": [
    "`self.classes_ = np.unique(y)`; for each class, `Nc = X[y == c].sum(axis=0)`.",
    "`feature_log_prob = np.log((Nc + a) / (Nc.sum() + a * V))`.",
    "Joint `= X @ flp.T + prior`; subtract the row log-sum-exp.",
],
"solution": r'''
import numpy as np


class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        V = X.shape[1]
        priors, flp = [], []
        for c in self.classes_:
            Xc = X[y == c]
            priors.append(np.log(len(Xc) / len(X)))
            Nc = Xc.sum(axis=0)
            flp.append(np.log((Nc + self.alpha) / (Nc.sum() + self.alpha * V)))
        self.class_log_prior_ = np.array(priors)
        self.feature_log_prob_ = np.array(flp)
        return self

    def predict_log_proba(self, X):
        J = np.asarray(X, dtype=float) @ self.feature_log_prob_.T + self.class_log_prior_
        m = J.max(axis=1, keepdims=True)
        return J - (m + np.log(np.exp(J - m).sum(axis=1, keepdims=True)))

    def predict(self, X):
        return self.classes_[self.predict_log_proba(X).argmax(axis=1)]
''',
"explanation": r'''
Training reduces to counting: class frequencies give priors, and smoothed per-class term counts
give word probabilities, all stored as logs. Prediction is a matrix product of counts with log
probabilities plus log priors, normalised with log-sum-exp; argmax picks the most probable class.
''',
"tests": r'''
import numpy as np

class TestNB(unittest.TestCase):
    def test_params(self):
        m = S.MultinomialNB().fit(np.array([[3, 0], [0, 2]]), np.array(["spam", "ham"]))
        self.assertEqual(list(m.classes_), ["ham", "spam"])
        np.testing.assert_allclose(np.exp(m.feature_log_prob_), [[0.25, 0.75], [0.8, 0.2]])
        np.testing.assert_allclose(np.exp(m.class_log_prior_), [0.5, 0.5])

    def test_predict(self):
        m = S.MultinomialNB().fit(np.array([[3, 0], [0, 2]]), np.array(["spam", "ham"]))
        self.assertEqual(list(m.predict(np.array([[1, 0], [0, 1]]))), ["spam", "ham"])

    def test_log_proba_normalised(self):
        rng = np.random.default_rng(0)
        X = rng.integers(0, 4, (12, 5)); y = rng.integers(0, 3, 12)
        lp = S.MultinomialNB().fit(X, y).predict_log_proba(X)
        np.testing.assert_allclose(np.exp(lp).sum(axis=1), 1.0)

    def test_smoothing_unseen_word(self):
        m = S.MultinomialNB(alpha=1.0).fit(np.array([[2, 0, 0], [0, 2, 0]]), np.array([0, 1]))
        self.assertTrue(np.isfinite(m.predict_log_proba(np.array([[0, 0, 5]]))).all())

    def test_prior_matters(self):
        X = np.array([[1, 1]] * 3 + [[1, 1]]); y = np.array([0, 0, 0, 1])
        m = S.MultinomialNB().fit(X, y)
        self.assertEqual(m.predict(np.array([[1, 1]]))[0], 0)

    def test_long_document_no_underflow(self):
        m = S.MultinomialNB().fit(np.array([[5, 1], [1, 5]]), np.array([0, 1]))
        lp = m.predict_log_proba(np.array([[3000, 2900]]))
        self.assertTrue(np.isfinite(lp).all())

    def test_bad_alpha(self):
        with self.assertRaises(ValueError):
            S.MultinomialNB(alpha=0).fit(np.ones((2, 2)), np.array([0, 1]))
''',
"feedback": [
    ("test_params", "θ = (N_ct + α)/(Σ_t N_ct + αV) per class, using term counts."),
    ("test_log_proba_normalised", "Subtract the log-sum-exp of each row."),
    ("test_smoothing_unseen_word", "Laplace smoothing must give unseen words a non-zero probability."),
    ("test_long_document_no_underflow", "Stay in log space; don't exponentiate before normalising."),
],
},
# ---------------------------------------------------------------- suffix-stemmer
{
"slug": "suffix-stemmer", "title": "Rule-Based Suffix Stemmer", "optional": True,
"difficulty": "advanced", "prereqs": ["tokenize-normalize"], "packages": [],
"objectives": ["Implement Porter's consonant/vowel definition and measure m",
               "Apply Porter Step 1a and Step 1b rules in order", "Understand why naive suffix stripping fails"],
"tags": ["stemming", "porter-stemmer", "morphology", "rules"],
"sources": ["S018", "S017"], "entry": "measure(stem); step1ab(word)",
"article": r'''
# The Porter Stemmer (Steps 1a–1b)

## Intuition
"connected", "connecting" and "connection" share a stem. Naively chopping "ing"/"ed" turns "sing"
into "s" and "bled" into "bl". The Porter stemmer (Porter, 1980) uses ordered rules with
conditions that look at the *shape* of the remaining stem.

## Precise explanation
**Consonants:** a letter other than a, e, i, o, u, and other than *y preceded by a consonant*. So
"y" in "toy" is a consonant (preceded by vowel o); in "syzygy" the middle y's are vowels.
Writing consonant runs as C and vowel runs as V, every word is $[C](VC)^m[V]$; $m$ is the
**measure**: tree → m = 0, trouble → 1, oaten → 2.

Conditions: `*v*` = stem contains a vowel; `*d` = ends in a double consonant; `*o` = ends
consonant-vowel-consonant where the last consonant is not w, x or y.

**Step 1a** (first matching suffix): SSES→SS, IES→I, SS→SS, S→"".
**Step 1b** (first matching suffix; a rule whose condition fails stops the step):
* (m > 0) EED → EE
* (*v*) ED → ""
* (*v*) ING → ""
If ED or ING was removed, tidy up: AT→ATE, BL→BLE, IZ→IZE; else if *d and not ending in l, s or
z → drop the last letter; else if m = 1 and *o → add E.

## Worked examples (from Porter's paper)
caresses→caress, ponies→poni, cats→cat, feed→feed, agreed→agree, plastered→plaster, bled→bled,
motoring→motor, sing→sing, conflated→conflate, hopping→hop, falling→fall, filing→file.

## Common mistakes
* Applying ED/ING without checking the remaining stem has a vowel ("bled" → "bl").
* Trying ED after an EED rule matched but failed its condition (feed must stay feed).
* Wrong y handling in the consonant test.

## Why this matters
Stemming reduces vocabulary size for search and classic text classification; implementing the
rules teaches careful, condition-driven string processing.
''',
"statement": r'''
Implement for lowercase ASCII words:
* `measure(stem)` → Porter's m.
* `step1ab(word)` → result of Porter Step 1a then Step 1b exactly as described.

**Examples**
```python
measure("tree"), measure("trouble"), measure("oaten")   # (0, 1, 2)
step1ab("caresses"), step1ab("ponies"), step1ab("feed"), step1ab("agreed")
# ('caress', 'poni', 'feed', 'agree')
step1ab("hopping"), step1ab("filing"), step1ab("sing")  # ('hop', 'file', 'sing')
```
''',
"starter": r'''
def is_consonant(word, i):
    # TODO
    pass


def measure(stem):
    # TODO
    pass


def step1ab(word):
    # TODO
    return word
''',
"hints": [
    "`is_consonant`: vowels aeiou → False; 'y' → True at i = 0, else `not is_consonant(word, i-1)`.",
    "Build a C/V pattern string, collapse runs, and count occurrences of 'VC'.",
    "Write helpers `has_vowel`, `ends_double_consonant`, `ends_cvc`; apply rules with `str.endswith`.",
],
"solution": r'''
def is_consonant(word, i):
    ch = word[i]
    if ch in "aeiou":
        return False
    if ch == "y":
        return i == 0 or not is_consonant(word, i - 1)
    return True


def measure(stem):
    pattern = "".join("C" if is_consonant(stem, i) else "V" for i in range(len(stem)))
    collapsed = ""
    for ch in pattern:
        if not collapsed or collapsed[-1] != ch:
            collapsed += ch
    return collapsed.count("VC")


def _has_vowel(stem):
    return any(not is_consonant(stem, i) for i in range(len(stem)))


def _ends_double_consonant(w):
    return len(w) >= 2 and w[-1] == w[-2] and is_consonant(w, len(w) - 1)


def _ends_cvc(w):
    if len(w) < 3:
        return False
    n = len(w)
    return (is_consonant(w, n - 3) and not is_consonant(w, n - 2)
            and is_consonant(w, n - 1) and w[-1] not in "wxy")


def step1ab(word):
    w = word
    # Step 1a
    if w.endswith("sses"):
        w = w[:-2]
    elif w.endswith("ies"):
        w = w[:-2]
    elif w.endswith("ss"):
        pass
    elif w.endswith("s"):
        w = w[:-1]
    # Step 1b
    removed = False
    if w.endswith("eed"):
        if measure(w[:-3]) > 0:
            w = w[:-1]
    elif w.endswith("ed") and _has_vowel(w[:-2]):
        w, removed = w[:-2], True
    elif w.endswith("ing") and _has_vowel(w[:-3]):
        w, removed = w[:-3], True
    if removed:
        if w.endswith(("at", "bl", "iz")):
            w = w + "e"
        elif _ends_double_consonant(w) and w[-1] not in "lsz":
            w = w[:-1]
        elif measure(w) == 1 and _ends_cvc(w):
            w = w + "e"
    return w
''',
"explanation": r'''
`is_consonant` encodes Porter's y-rule recursively. The measure collapses the C/V pattern into
alternating runs and counts VC pairs. Step 1a picks the first matching suffix. In Step 1b, an EED
match blocks the ED rule even when its m > 0 condition fails (so "feed" stays "feed"), and the
tidy-up rules run only after ED or ING was actually removed.
''',
"tests": r'''
PAIRS_1A = {"caresses": "caress", "ponies": "poni", "ties": "ti", "caress": "caress", "cats": "cat"}
PAIRS_1B = {"feed": "feed", "agreed": "agree", "plastered": "plaster", "bled": "bled",
            "motoring": "motor", "sing": "sing", "conflated": "conflate", "troubled": "trouble",
            "sized": "size", "hopping": "hop", "tanned": "tan", "falling": "fall",
            "hissing": "hiss", "fizzed": "fizz", "failing": "fail", "filing": "file"}

class TestPorter(unittest.TestCase):
    def test_measure(self):
        for w, m in {"tr": 0, "tree": 0, "y": 0, "by": 0, "trouble": 1, "oats": 1, "trees": 1,
                     "ivy": 1, "troubles": 2, "private": 2, "oaten": 2, "orrery": 2}.items():
            self.assertEqual(S.measure(w), m, w)

    def test_y_consonant(self):
        self.assertTrue(S.is_consonant("toy", 2))
        self.assertFalse(S.is_consonant("syzygy", 1))
        self.assertTrue(S.is_consonant("yes", 0))

    def test_step1a(self):
        for w, e in PAIRS_1A.items():
            self.assertEqual(S.step1ab(w), e, w)

    def test_step1b(self):
        for w, e in PAIRS_1B.items():
            self.assertEqual(S.step1ab(w), e, w)

    def test_eed_blocks_ed(self):
        self.assertEqual(S.step1ab("feed"), "feed")

    def test_no_vowel_stem_kept(self):
        self.assertEqual(S.step1ab("bled"), "bled")
        self.assertEqual(S.step1ab("sing"), "sing")

    def test_short(self):
        self.assertEqual(S.step1ab("s"), "")
        self.assertEqual(S.step1ab("as"), "a")
''',
"feedback": [
    ("test_measure", "Collapse the C/V pattern to runs and count 'VC' occurrences."),
    ("test_y_consonant", "y is a consonant at the start or after a vowel; a vowel after a consonant."),
    ("test_eed_blocks_ed", "If the word ends in 'eed', only the EED rule is considered."),
    ("test_step1b", "Tidy-up rules (ATE/BLE/IZE, double consonant, *o + E) apply only after ED/ING removal."),
],
},
# ---------------------------------------------------------------- embedding-analogy
{
"slug": "embedding-analogy", "title": "Word Embedding Analogies",
"difficulty": "advanced", "prereqs": ["nlp-tfidf-retrieval", "ppmi-matrix"], "packages": ["numpy"],
"objectives": ["Find nearest neighbours in embedding space", "Solve analogies with vector arithmetic (3CosAdd)",
               "Exclude query words from results"],
"tags": ["word-embeddings", "analogies", "cosine-similarity", "vector-arithmetic"],
"sources": ["S017", "S013"], "entry": "most_similar(word, emb, k=3); analogy(a, b, c, emb)",
"article": r'''
# Word Embeddings and Analogies

## Intuition
Embeddings place words as points so that similar words are close. Remarkably, consistent
*directions* can appear: the offset from "man" to "woman" resembles the offset from "king" to
"queen". "a is to b as c is to ?" becomes vector arithmetic.

## Precise explanation
**Nearest neighbours:** rank words by cosine similarity ([[cosine-retrieval]]) to a query vector.
**3CosAdd analogy:** answer $d^* = \arg\max_{d \notin \{a,b,c\}} \cos(v_d,\ v_b - v_a + v_c)$.
Excluding a, b, c is essential: the target vector is usually closest to b or c themselves.
Real embeddings (word2vec, GloVe) have 100–300 dimensions; analogies work for some relations and
fail for many — they are a probe, not a guarantee.

## Worked example
Toy 3-D embeddings: man [1,0,0], woman [1,1,0], king [1,0,1], queen [1,1,1]:
woman − man + king = [1,1,1] → queen (cos 1).

## Common mistakes
* Not excluding the input words.
* Euclidean distance on unnormalised vectors (frequency effects dominate).
* Over-interpreting analogy results as "understanding".

## Why this matters
Embedding lookup is the first layer of every LLM; similarity search over embeddings drives
semantic retrieval.
''',
"statement": r'''
`emb` is a dict word → 1-D NumPy vector (same length). Implement:
* `most_similar(word, emb, k=3)` → list of `(other_word, cosine)` for the k most similar *other*
  words, highest first, ties alphabetical. Raise `KeyError` for unknown words.
* `analogy(a, b, c, emb)` → the word d (not a, b or c) maximising cosine with `v_b - v_a + v_c`
  (ties alphabetical).

Zero vectors have cosine 0 with everything.

**Example**
```python
emb = {"man": np.array([1., 0, 0]), "woman": np.array([1., 1, 0]),
       "king": np.array([1., 0, 1]), "queen": np.array([1., 1, 1])}
analogy("man", "woman", "king", emb)   # 'queen'
```
''',
"starter": r'''
import numpy as np


def most_similar(word, emb, k=3):
    # TODO
    return []


def analogy(a, b, c, emb):
    # TODO
    pass
''',
"hints": [
    "Write `_cos(u, v)` returning 0 if either norm is 0.",
    "Score every candidate and sort with key `(-score, word)`.",
    "Target vector: `emb[b] - emb[a] + emb[c]`; skip {a, b, c}.",
],
"solution": r'''
import numpy as np


def _cos(u, v):
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu == 0 or nv == 0:
        return 0.0
    return float(u @ v / (nu * nv))


def _rank(target, emb, exclude):
    scored = [(w, _cos(target, v)) for w, v in emb.items() if w not in exclude]
    return sorted(scored, key=lambda t: (-t[1], t[0]))


def most_similar(word, emb, k=3):
    if word not in emb:
        raise KeyError(word)
    return _rank(emb[word], emb, {word})[:k]


def analogy(a, b, c, emb):
    for w in (a, b, c):
        if w not in emb:
            raise KeyError(w)
    ranked = _rank(emb[b] - emb[a] + emb[c], emb, {a, b, c})
    if not ranked:
        raise ValueError("no candidate words")
    return ranked[0][0]
''',
"explanation": r'''
A shared ranking helper scores candidates by cosine with a target vector, excluding given words,
and sorts by score then name. Similarity search uses the word's own vector; analogies use the
3CosAdd offset vector.
''',
"tests": r'''
import numpy as np

EMB = {"man": np.array([1., 0, 0]), "woman": np.array([1., 1, 0]),
       "king": np.array([1., 0, 1]), "queen": np.array([1., 1, 1]),
       "apple": np.array([0., 0, -1]), "zero": np.zeros(3)}

class TestEmbeddings(unittest.TestCase):
    def test_analogy(self):
        self.assertEqual(S.analogy("man", "woman", "king", EMB), "queen")

    def test_analogy_reverse(self):
        self.assertEqual(S.analogy("woman", "man", "queen", EMB), "king")

    def test_excludes_inputs(self):
        emb = {"a": np.array([1., 0]), "b": np.array([1., 0.1]), "c": np.array([0., 1]), "d": np.array([-1., 0])}
        self.assertNotIn(S.analogy("a", "b", "c", emb), {"a", "b", "c"})

    def test_most_similar(self):
        r = S.most_similar("king", EMB, k=2)
        self.assertEqual(r[0][0], "queen")
        self.assertAlmostEqual(r[0][1], 2 / np.sqrt(6))
        self.assertNotIn("king", [w for w, _ in S.most_similar("king", EMB, k=10)])

    def test_zero_vector(self):
        self.assertEqual(dict(S.most_similar("man", EMB, k=10))["zero"], 0.0)

    def test_ties_alphabetical(self):
        emb = {"q": np.array([1., 0]), "b": np.array([0., 1]), "a": np.array([0., -1])}
        self.assertEqual([w for w, _ in S.most_similar("q", emb, k=2)], ["a", "b"])

    def test_unknown(self):
        with self.assertRaises(KeyError):
            S.most_similar("xyz", EMB)
''',
"feedback": [
    ("test_analogy", "Target = v_b − v_a + v_c; rank by cosine."),
    ("test_excludes_inputs", "Exclude a, b and c from the candidates."),
    ("test_zero_vector", "Return cosine 0 for zero vectors instead of NaN."),
    ("test_ties_alphabetical", "Sort by (−score, word)."),
],
},
# ---------------------------------------------------------------- ppmi-matrix
{
"slug": "ppmi-matrix", "title": "PPMI Co-occurrence Matrix",
"difficulty": "advanced", "prereqs": ["bag-of-words", "tf-idf"], "packages": ["numpy"],
"objectives": ["Count word–context co-occurrences in a window", "Compute positive pointwise mutual information",
               "Use PPMI rows as word vectors"],
"tags": ["co-occurrence", "ppmi", "distributional-semantics", "word-vectors"],
"sources": ["S017"], "entry": "cooccurrence(sentences, vocab, window=2); ppmi(C)",
"article": r'''
# Distributional Vectors with PPMI

## Intuition
"You shall know a word by the company it keeps." Count which words appear near each word; words
with similar neighbours get similar count vectors. Raw counts are dominated by frequent words, so
we reweight by how *surprising* each co-occurrence is.

## Precise explanation
**Co-occurrence:** for each token at position i, every token within distance `window` on either
side (same sentence, excluding itself) is a context: $C[w, c] \mathrel{+}= 1$. The matrix is
symmetric for a symmetric window.
**PMI:** $\text{PMI}(w, c) = \log_2 \frac{P(w,c)}{P(w)P(c)}$ with
$P(w,c) = C_{wc}/N$, $P(w) = \sum_c C_{wc}/N$, $P(c) = \sum_w C_{wc}/N$, $N = \sum C$.
**PPMI** $= \max(\text{PMI}, 0)$; cells with $C_{wc} = 0$ are 0 (avoid $\log 0$).
Positive values mean "co-occur more than chance".

## Worked example
Sentences [a b], [a c], window 1: C(a,b) = C(b,a) = C(a,c) = C(c,a) = 1, N = 4. P(a, b) = 1/4,
P(a) = 2/4, P(b) = 1/4 → PMI = log2((1/4)/(1/2 · 1/4)) = 1.

## Common mistakes
* Crossing sentence boundaries.
* Counting the word as its own context.
* Taking log of zero.

## Why this matters
PPMI + cosine is a classic count-based embedding; word2vec has been shown to be closely related
to factorising a shifted PMI matrix.
''',
"statement": r'''
Implement:
* `cooccurrence(sentences, vocab, window=2)` → int matrix `(V, V)` with `vocab` a dict word → index;
  tokens not in vocab are skipped as targets **and** contexts but still occupy positions.
  Raise `ValueError` if `window < 1`.
* `ppmi(C)` → float PPMI matrix (log base 2, zeros where C is 0). Raise `ValueError` if `C.sum() == 0`.

**Example**
```python
vocab = {"a": 0, "b": 1, "c": 2}
C = cooccurrence([["a", "b"], ["a", "c"]], vocab, window=1)   # [[0,1,1],[1,0,0],[1,0,0]]
ppmi(C)[0, 1]    # 1.0
```
''',
"starter": r'''
import numpy as np


def cooccurrence(sentences, vocab, window=2):
    # TODO
    pass


def ppmi(C):
    # TODO
    pass
''',
"hints": [
    "For each i, loop `j in range(max(0, i - window), min(len(s), i + window + 1))`, skipping j == i.",
    "`P = C / N`, `pw = P.sum(1, keepdims=True)`, `pc = P.sum(0, keepdims=True)`.",
    "Compute log2 only where C > 0: `np.log2(P / (pw * pc), where=C > 0, out=np.zeros_like(P))`, then clip at 0.",
],
"solution": r'''
import numpy as np


def cooccurrence(sentences, vocab, window=2):
    if window < 1:
        raise ValueError("window must be >= 1")
    V = len(vocab)
    C = np.zeros((V, V), dtype=int)
    for s in sentences:
        for i, w in enumerate(s):
            if w not in vocab:
                continue
            for j in range(max(0, i - window), min(len(s), i + window + 1)):
                if j != i and s[j] in vocab:
                    C[vocab[w], vocab[s[j]]] += 1
    return C


def ppmi(C):
    C = np.asarray(C, dtype=float)
    N = C.sum()
    if N == 0:
        raise ValueError("empty co-occurrence matrix")
    P = C / N
    pw = P.sum(axis=1, keepdims=True)
    pc = P.sum(axis=0, keepdims=True)
    denom = pw * pc
    pmi = np.zeros_like(P)
    mask = C > 0
    np.log2(P / np.where(denom > 0, denom, 1.0), out=pmi, where=mask)
    return np.maximum(pmi, 0.0)
''',
"explanation": r'''
Counting walks a symmetric window inside each sentence, skipping the centre and out-of-vocabulary
tokens (which still keep their positions). PPMI converts counts to joint and marginal probabilities
and takes log2 only where counts are positive, clipping negatives to zero.
''',
"tests": r'''
import numpy as np

V = {"a": 0, "b": 1, "c": 2}

class TestPPMI(unittest.TestCase):
    def test_counts(self):
        C = S.cooccurrence([["a", "b"], ["a", "c"]], V, window=1)
        np.testing.assert_array_equal(C, [[0, 1, 1], [1, 0, 0], [1, 0, 0]])

    def test_window(self):
        C = S.cooccurrence([["a", "b", "c"]], V, window=1)
        self.assertEqual(C[0, 2], 0)
        self.assertEqual(S.cooccurrence([["a", "b", "c"]], V, window=2)[0, 2], 1)

    def test_oov_positions(self):
        C = S.cooccurrence([["a", "zzz", "c"]], V, window=1)
        self.assertEqual(C.sum(), 0)

    def test_symmetric(self):
        C = S.cooccurrence([["a", "b", "a", "c", "b"]], V, window=2)
        np.testing.assert_array_equal(C, C.T)

    def test_ppmi_value(self):
        P = S.ppmi(S.cooccurrence([["a", "b"], ["a", "c"]], V, window=1))
        self.assertAlmostEqual(P[0, 1], 1.0)
        self.assertEqual(P[1, 2], 0.0)

    def test_ppmi_nonneg_finite(self):
        rng = np.random.default_rng(0)
        C = rng.integers(0, 5, (6, 6))
        P = S.ppmi(C)
        self.assertTrue(np.isfinite(P).all() and (P >= 0).all())
        self.assertTrue((P[C == 0] == 0).all())

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.ppmi(np.zeros((2, 2)))
        with self.assertRaises(ValueError):
            S.cooccurrence([["a"]], V, window=0)
''',
"feedback": [
    ("test_counts", "Count neighbours within the window inside each sentence, excluding the word itself."),
    ("test_oov_positions", "OOV tokens still occupy positions; don't delete them before windowing."),
    ("test_ppmi_value", "PMI = log2(P(w,c) / (P(w)P(c))) with marginals from row/column sums."),
    ("test_ppmi_nonneg_finite", "Only take logs where C > 0 and clip negatives to 0."),
],
},
]

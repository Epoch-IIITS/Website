"""Problem definitions for the llms topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- bigram-next-token
{
"slug": "bigram-next-token", "title": "Next-Token Probabilities (Add-k)",
"difficulty": "beginner", "prereqs": ["token-ids", "tokenize-normalize"], "packages": [],
"objectives": ["Frame language modelling as next-token prediction", "Apply add-k smoothing",
               "Return a full distribution over the vocabulary"],
"tags": ["language-modeling", "next-token", "smoothing", "n-grams"],
"sources": ["S017"], "entry": "next_token_dist(bigrams, prev, vocab, k=1.0)",
"article": r'''
# Next-Token Prediction

## Intuition
An LLM is, at its core, a function that maps a context to a probability distribution over the next
token. A bigram model is the simplest such function: the context is just the previous token.

## Precise explanation
With bigram counts $C(\text{prev}, w)$ ([[bigram-counts]]) and vocabulary size $V$, **add-k smoothing** gives
$$P(w\mid\text{prev}) = \frac{C(\text{prev}, w) + k}{\sum_{w'} C(\text{prev}, w') + kV}.$$
* k = 0 is the MLE (zero probability for unseen pairs, undefined for unseen contexts).
* k = 1 is Laplace smoothing; smaller k (0.1, 0.01) usually works better.
* An unseen context gets the uniform distribution $1/V$.
Every distribution must sum to 1 over the whole vocabulary — the same contract an LLM's softmax
output satisfies.

## Worked example
Counts after "like": tea 1, coffee 1; V = 4 ({tea, coffee, i, like}); k = 1:
P(tea) = 2/6, P(coffee) = 2/6, P(i) = 1/6, P(like) = 1/6.

## Common mistakes
* Adding k to the numerator but forgetting kV in the denominator.
* Returning only seen words (the distribution must cover the vocabulary).
* Using a vocabulary that differs between training and evaluation.

## Why this matters
Perplexity ([[perplexity]]), sampling ([[top-k-top-p]]) and beam search ([[beam-search]]) all consume exactly this kind of
next-token distribution.
''',
"statement": r'''
Write `next_token_dist(bigrams, prev, vocab, k=1.0)` where `bigrams` maps `(prev, word)` → count.
Return a dict over **every** word in `vocab` (a list) with add-k probabilities. Raise `ValueError`
if `k < 0`, or if `k == 0` and `prev` has no observed bigrams.

**Example**
```python
b = {("like", "tea"): 1, ("like", "coffee"): 1, ("i", "like"): 2}
next_token_dist(b, "like", ["tea", "coffee", "i", "like"])
# {'tea': 0.333.., 'coffee': 0.333.., 'i': 0.1666.., 'like': 0.1666..}
```
''',
"starter": r'''
def next_token_dist(bigrams, prev, vocab, k=1.0):
    # TODO
    return {}
''',
"hints": [
    "Context total: `sum(bigrams.get((prev, w), 0) for w in vocab)`.",
    "Denominator: `total + k * len(vocab)`.",
    "`{w: (bigrams.get((prev, w), 0) + k) / denom for w in vocab}`.",
],
"solution": r'''
def next_token_dist(bigrams, prev, vocab, k=1.0):
    if k < 0:
        raise ValueError("k must be >= 0")
    counts = {w: bigrams.get((prev, w), 0) for w in vocab}
    total = sum(counts.values())
    denom = total + k * len(vocab)
    if denom == 0:
        raise ValueError("unseen context with k = 0")
    return {w: (c + k) / denom for w, c in counts.items()}
''',
"explanation": r'''
Counts for the context are gathered over the full vocabulary, k pseudo-counts are added to each
word, and everything is divided by the adjusted total, which guarantees a proper distribution.
''',
"tests": r'''
B = {("like", "tea"): 1, ("like", "coffee"): 1, ("i", "like"): 2}
VOCAB = ["tea", "coffee", "i", "like"]

class TestNextToken(unittest.TestCase):
    def test_example(self):
        d = S.next_token_dist(B, "like", VOCAB)
        self.assertAlmostEqual(d["tea"], 2 / 6)
        self.assertAlmostEqual(d["i"], 1 / 6)

    def test_sums_to_one(self):
        for prev in ["like", "i", "tea", "unknown"]:
            self.assertAlmostEqual(sum(S.next_token_dist(B, prev, VOCAB, 0.5).values()), 1.0)

    def test_full_vocab(self):
        self.assertEqual(set(S.next_token_dist(B, "i", VOCAB)), set(VOCAB))

    def test_unseen_context_uniform(self):
        d = S.next_token_dist(B, "zzz", VOCAB)
        for v in d.values():
            self.assertAlmostEqual(v, 0.25)

    def test_mle(self):
        d = S.next_token_dist(B, "i", VOCAB, k=0)
        self.assertEqual(d["like"], 1.0)
        self.assertEqual(d["tea"], 0.0)

    def test_mle_unseen_raises(self):
        with self.assertRaises(ValueError):
            S.next_token_dist(B, "zzz", VOCAB, k=0)

    def test_smaller_k_sharper(self):
        a = S.next_token_dist(B, "i", VOCAB, 1.0)["like"]
        b = S.next_token_dist(B, "i", VOCAB, 0.1)["like"]
        self.assertGreater(b, a)
''',
"feedback": [
    ("test_example", "Denominator is total + k·V."),
    ("test_full_vocab", "Return a probability for every vocabulary word."),
    ("test_unseen_context_uniform", "An unseen context with k > 0 gives 1/V for each word."),
    ("test_mle_unseen_raises", "With k = 0 and no counts the distribution is undefined — raise ValueError."),
],
},
# ---------------------------------------------------------------- temperature-softmax
{
"slug": "temperature-softmax", "title": "Logits, Temperature and Softmax",
"difficulty": "beginner", "prereqs": ["bigram-next-token", "stable-softmax"], "packages": ["numpy"],
"objectives": ["Convert logits to probabilities with temperature", "Measure distribution sharpness with entropy",
               "Explain the T → 0 and T → ∞ limits"],
"tags": ["temperature", "softmax", "entropy", "decoding"],
"sources": ["S013", "S021"], "entry": "softmax_t(logits, T=1.0); entropy(p)",
"article": r'''
# Temperature

## Intuition
Temperature is a "creativity knob". Dividing logits by T before softmax sharpens (T < 1) or
flattens (T > 1) the distribution. Low T → confident, repetitive text; high T → diverse, sometimes
nonsensical text.

## Precise explanation
$$p_i(T) = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}},\qquad T > 0.$$
* T = 1: ordinary softmax.
* T → 0: all mass on the argmax (greedy decoding, [[greedy-decoding]]).
* T → ∞: uniform.
Ranking of tokens never changes — only how peaked the distribution is.
**Entropy** $H(p) = -\sum p_i \log p_i$ (nats; terms with $p_i = 0$ contribute 0) measures
spread: 0 for one-hot, $\log V$ for uniform. Entropy increases with T.

## Worked example
z = [2, 1, 0]: T = 1 → [0.665, 0.245, 0.090]; T = 0.5 → [0.867, 0.117, 0.016];
T = 10 → ≈ [0.367, 0.332, 0.301].

## Common mistakes
* Multiplying instead of dividing by T.
* Allowing T = 0 (division by zero) — treat greedy decoding separately.
* Computing entropy with `log(0)` → NaN.

## Why this matters
Temperature is a standard generation setting in LLM APIs and interacts with top-k/top-p
filtering ([[top-k-top-p]]).
''',
"statement": r'''
Implement:
* `softmax_t(logits, T=1.0)` → stable softmax of `logits / T` (1-D); raise `ValueError` if `T <= 0`.
* `entropy(p)` → natural-log entropy of a probability vector (0·log 0 treated as 0).

**Examples**
```python
softmax_t(np.array([2., 1., 0.]), 0.5)   # [0.8668, 0.1173, 0.0159]
entropy(np.array([0.5, 0.5]))            # 0.6931...
entropy(np.array([1.0, 0.0]))            # 0.0
```
''',
"starter": r'''
import numpy as np


def softmax_t(logits, T=1.0):
    pass


def entropy(p):
    pass
''',
"hints": [
    "`z = np.asarray(logits, float) / T`, subtract the max, exponentiate, normalise.",
    "Entropy: use only `p > 0` entries: `-(p[p > 0] * np.log(p[p > 0])).sum()`.",
    "Validate T before dividing.",
],
"solution": r'''
import numpy as np


def softmax_t(logits, T=1.0):
    if T <= 0:
        raise ValueError("temperature must be positive")
    z = np.asarray(logits, dtype=float) / T
    e = np.exp(z - z.max())
    return e / e.sum()


def entropy(p):
    p = np.asarray(p, dtype=float)
    nz = p[p > 0]
    return float(-(nz * np.log(nz)).sum())
''',
"explanation": r'''
Scaling logits by 1/T before a stable softmax implements temperature. Entropy ignores zero
entries, matching the 0·log 0 = 0 convention.
''',
"tests": r'''
import numpy as np

Z = np.array([2., 1., 0.])

class TestTemp(unittest.TestCase):
    def test_t1(self):
        np.testing.assert_allclose(S.softmax_t(Z), np.exp(Z) / np.exp(Z).sum())

    def test_t_half(self):
        np.testing.assert_allclose(S.softmax_t(Z, 0.5), np.exp(2 * Z) / np.exp(2 * Z).sum())

    def test_low_t_greedy(self):
        p = S.softmax_t(Z, 0.01)
        self.assertAlmostEqual(p[0], 1.0, places=9)

    def test_high_t_uniform(self):
        np.testing.assert_allclose(S.softmax_t(Z, 1e6), [1 / 3] * 3, atol=1e-6)

    def test_rank_preserved(self):
        for T in (0.2, 1.0, 5.0):
            self.assertEqual(list(np.argsort(S.softmax_t(Z, T))), [2, 1, 0])

    def test_entropy(self):
        self.assertAlmostEqual(S.entropy(np.array([0.5, 0.5])), np.log(2))
        self.assertEqual(S.entropy(np.array([1.0, 0.0])), 0.0)

    def test_entropy_increases_with_t(self):
        hs = [S.entropy(S.softmax_t(Z, T)) for T in (0.3, 1.0, 3.0)]
        self.assertTrue(hs[0] < hs[1] < hs[2])

    def test_bad_t(self):
        with self.assertRaises(ValueError):
            S.softmax_t(Z, 0)
''',
"feedback": [
    ("test_t_half", "Divide logits by T (T = 0.5 doubles them)."),
    ("test_entropy", "Skip zero probabilities to avoid log(0)."),
    ("test_low_t_greedy", "Use the max-subtraction trick so tiny T does not overflow."),
    ("test_bad_t", "T must be > 0."),
],
},
# ---------------------------------------------------------------- greedy-decoding
{
"slug": "greedy-decoding", "title": "Greedy Decoding",
"difficulty": "beginner", "prereqs": ["temperature-softmax"], "packages": ["numpy"],
"objectives": ["Run an autoregressive generation loop", "Stop on an end-of-sequence token or a length limit",
               "Recognise repetition loops in greedy output"],
"tags": ["decoding", "greedy", "autoregressive", "generation"],
"sources": ["S013", "S022"], "entry": "greedy_decode(next_logits, prompt, vocab, eos='</s>', max_new=20)",
"article": r'''
# Autoregressive Generation: Greedy Decoding

## Intuition
A language model writes one token at a time: look at everything so far, pick the next token,
append it, repeat. **Greedy** decoding always picks the single most likely token.

## Precise explanation
```text
tokens = prompt
repeat up to max_new times:
    logits = model(tokens)          # scores for every vocabulary entry
    t = vocab[argmax(logits)]       # ties → lowest index
    append t
    if t == eos: stop
```
Greedy decoding is deterministic and fast but can loop ("the the the …") or miss better overall
sequences that start with a less likely token — beam search ([[beam-search]]) and sampling ([[top-k-top-p]]) address
this.

```mermaid
flowchart LR
  P[prompt] --> M[model: next-token logits] --> A[argmax] --> T[append token]
  T --> C{eos or max_new?}
  C -- no --> M
  C -- yes --> O[output]
```

## Worked example
A toy model where "i"→"like", "like"→"tea", "tea"→"</s>": prompt ["i"] → ["i", "like", "tea", "</s>"].

## Common mistakes
* Forgetting to feed the *updated* sequence back into the model.
* Not stopping at EOS, or stopping before appending it.
* Infinite loops without `max_new`.

## Why this matters
Every chatbot reply is produced by such a loop; understanding it explains latency (one model call
per token) and the KV cache optimisation ([[kv-cache]]).
''',
"statement": r'''
Write `greedy_decode(next_logits, prompt, vocab, eos="</s>", max_new=20)`:
* `next_logits(tokens)` returns a 1-D array of scores aligned with `vocab` (a list).
* Generate until the chosen token is `eos` (it is appended) or `max_new` tokens were added.
* Return the full token list (prompt + generated). Ties → lowest vocabulary index.
* Raise `ValueError` if `max_new < 0` or the logits length differs from `len(vocab)`.

**Example**
```python
vocab = ["i", "like", "tea", "</s>"]
table = {"i": [0, 5, 1, 0], "like": [0, 0, 3, 1], "tea": [0, 0, 0, 9]}
f = lambda toks: np.array(table[toks[-1]], float)
greedy_decode(f, ["i"], vocab)    # ['i', 'like', 'tea', '</s>']
```
''',
"starter": r'''
import numpy as np


def greedy_decode(next_logits, prompt, vocab, eos="</s>", max_new=20):
    # TODO
    return list(prompt)
''',
"hints": [
    "`tokens = list(prompt)`; loop `for _ in range(max_new)`.",
    "`z = np.asarray(next_logits(tokens))`; `t = vocab[int(np.argmax(z))]` (argmax returns the first max).",
    "Append, then `break` if `t == eos`.",
],
"solution": r'''
import numpy as np


def greedy_decode(next_logits, prompt, vocab, eos="</s>", max_new=20):
    if max_new < 0:
        raise ValueError("max_new must be >= 0")
    tokens = list(prompt)
    for _ in range(max_new):
        z = np.asarray(next_logits(tokens), dtype=float)
        if z.shape != (len(vocab),):
            raise ValueError("logits must align with vocab")
        t = vocab[int(np.argmax(z))]
        tokens.append(t)
        if t == eos:
            break
    return tokens
''',
"explanation": r'''
Each iteration calls the model on the full current sequence, appends the argmax token and stops at
EOS. `np.argmax` returns the first maximum, giving the lowest-index tie-break. The step budget
guarantees termination.
''',
"tests": r'''
import numpy as np

VOCAB = ["i", "like", "tea", "</s>"]
TABLE = {"i": [0, 5, 1, 0], "like": [0, 0, 3, 1], "tea": [0, 0, 0, 9], "</s>": [1, 0, 0, 0]}
F = lambda toks: np.array(TABLE[toks[-1]], float)

class TestGreedy(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.greedy_decode(F, ["i"], VOCAB), ["i", "like", "tea", "</s>"])

    def test_max_new(self):
        self.assertEqual(S.greedy_decode(F, ["i"], VOCAB, max_new=2), ["i", "like", "tea"])

    def test_zero_new(self):
        self.assertEqual(S.greedy_decode(F, ["i"], VOCAB, max_new=0), ["i"])

    def test_loop_capped(self):
        loop = lambda toks: np.array([0, 1, 0, 0], float)
        self.assertEqual(S.greedy_decode(loop, ["i"], VOCAB, max_new=3), ["i", "like", "like", "like"])

    def test_tie_lowest_index(self):
        tie = lambda toks: np.array([0, 2, 2, 0], float) if len(toks) < 2 else np.array([0, 0, 0, 1], float)
        self.assertEqual(S.greedy_decode(tie, ["i"], VOCAB), ["i", "like", "</s>"])

    def test_uses_full_context(self):
        seen = []
        def f(toks):
            seen.append(list(toks)); return np.array([0, 0, 0, 1], float)
        S.greedy_decode(f, ["i", "like"], VOCAB)
        self.assertEqual(seen, [["i", "like"]])

    def test_prompt_not_mutated(self):
        p = ["i"]
        S.greedy_decode(F, p, VOCAB)
        self.assertEqual(p, ["i"])

    def test_bad_logits(self):
        with self.assertRaises(ValueError):
            S.greedy_decode(lambda t: np.zeros(3), ["i"], VOCAB)
''',
"feedback": [
    ("test_example", "Append the argmax token and stop after appending EOS."),
    ("test_max_new", "Generate at most max_new new tokens."),
    ("test_uses_full_context", "Pass the whole current sequence to the model."),
    ("test_prompt_not_mutated", "Copy the prompt before appending."),
],
},
# ---------------------------------------------------------------- perplexity
{
"slug": "perplexity", "title": "Perplexity",
"difficulty": "beginner", "prereqs": ["bigram-next-token", "cross-entropy"], "packages": [],
"objectives": ["Compute average negative log-likelihood per token", "Convert it to perplexity",
               "Interpret perplexity as an effective branching factor"],
"tags": ["perplexity", "evaluation", "cross-entropy", "language-modeling"],
"sources": ["S017"], "entry": "avg_nll(token_probs); perplexity(token_probs)",
"article": r'''
# Perplexity

## Intuition
If a model is as uncertain as rolling a fair 10-sided die for every token, its perplexity is 10.
Lower perplexity means the model finds the text less surprising.

## Precise explanation
Given the probabilities the model assigned to the **actual** next tokens, $p_1,\dots,p_N$:
$$\text{NLL} = -\frac1N\sum_i \ln p_i,\qquad \text{PPL} = e^{\text{NLL}}.$$
(Equivalently $2^{H}$ with $H$ in bits.) NLL is exactly the mean cross-entropy training loss
([[cross-entropy]]), so PPL = exp(loss). If any $p_i = 0$, the NLL is infinite and so is perplexity — one reason
smoothing ([[bigram-next-token]]) matters. Perplexities are only comparable for the **same tokenisation** and test
set.

## Worked example
p = [0.5, 0.25, 0.125]: NLL = (ln 2 + ln 4 + ln 8)/3 = 2 ln 2 → PPL = 4.
A uniform model over V tokens has PPL = V.

## Common mistakes
* Averaging probabilities instead of log-probabilities.
* Comparing perplexity across different tokenisers.
* Including padding tokens.

## Why this matters
Perplexity is the standard intrinsic metric for language models and appears in LLM technical
reports.
''',
"statement": r'''
Implement for a non-empty list of probabilities in `[0, 1]`:
* `avg_nll(token_probs)` → mean of `-ln p` (`math.inf` if any p is 0).
* `perplexity(token_probs)` → `exp(avg_nll)` (`math.inf` if infinite).
Raise `ValueError` for empty input or values outside `[0, 1]`.

**Examples**
```python
perplexity([0.5, 0.25, 0.125])   # 4.0
perplexity([0.1] * 7)            # 10.0
perplexity([0.9, 0.0])           # inf
```
''',
"starter": r'''
import math


def avg_nll(token_probs):
    pass


def perplexity(token_probs):
    pass
''',
"hints": [
    "Validate, then check `any(p == 0 for p in token_probs)`.",
    "`-sum(math.log(p) for p in token_probs) / len(token_probs)`.",
    "`math.exp(nll)` unless nll is inf.",
],
"solution": r'''
import math


def avg_nll(token_probs):
    if not token_probs:
        raise ValueError("need at least one probability")
    if any(not 0 <= p <= 1 for p in token_probs):
        raise ValueError("probabilities must be in [0, 1]")
    if any(p == 0 for p in token_probs):
        return math.inf
    return -sum(math.log(p) for p in token_probs) / len(token_probs)


def perplexity(token_probs):
    nll = avg_nll(token_probs)
    return math.inf if math.isinf(nll) else math.exp(nll)
''',
"explanation": r'''
The average negative log-probability is the per-token cross-entropy; exponentiating gives
perplexity. Zero probabilities make the log undefined, so infinity is returned explicitly.
''',
"tests": r'''
class TestPPL(unittest.TestCase):
    def test_example(self):
        self.assertAlmostEqual(S.perplexity([0.5, 0.25, 0.125]), 4.0)

    def test_uniform(self):
        self.assertAlmostEqual(S.perplexity([0.1] * 7), 10.0)

    def test_zero(self):
        self.assertEqual(S.perplexity([0.9, 0.0]), math.inf)
        self.assertEqual(S.avg_nll([0.0]), math.inf)

    def test_perfect(self):
        self.assertEqual(S.perplexity([1.0, 1.0]), 1.0)

    def test_nll_value(self):
        self.assertAlmostEqual(S.avg_nll([0.5, 0.25, 0.125]), 2 * math.log(2))

    def test_not_mean_of_probs(self):
        self.assertNotAlmostEqual(S.perplexity([0.9, 0.1]), 1 / 0.5)
        self.assertAlmostEqual(S.perplexity([0.9, 0.1]), 1 / math.sqrt(0.09))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.perplexity([])
        with self.assertRaises(ValueError):
            S.perplexity([1.2])
''',
"feedback": [
    ("test_example", "Average −ln p over tokens, then exponentiate."),
    ("test_not_mean_of_probs", "Perplexity is the inverse geometric mean, not 1 / arithmetic mean."),
    ("test_zero", "Return math.inf if any probability is 0."),
    ("test_invalid", "Validate empty input and range [0, 1]."),
],
},
# ---------------------------------------------------------------- bpe-merges
{
"slug": "bpe-merges", "title": "Byte-Pair Encoding Merges",
"difficulty": "intermediate", "prereqs": ["token-ids"], "packages": [],
"objectives": ["Count adjacent symbol pairs weighted by word frequency", "Learn BPE merges greedily",
               "Apply learned merges to segment a new word"],
"tags": ["bpe", "subword-tokenization", "tokenizers"],
"sources": ["S020", "S022"], "entry": "learn_bpe(word_counts, num_merges); apply_bpe(word, merges)",
"article": r'''
# Byte-Pair Encoding (BPE)

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
''',
"statement": r'''
Implement:
* `learn_bpe(word_counts, num_merges)` → list of merged pairs `(a, b)` in order. `word_counts` is a
  dict word → count. Each word starts as `tuple(word) + ("</w>",)`. Stop early if no pairs remain.
  Ties → smallest pair in Python tuple ordering.
* `apply_bpe(word, merges)` → list of symbols after applying merges in order.

**Example**
```python
m = learn_bpe({"low": 5, "lower": 2, "newest": 6, "widest": 3}, 3)
m                                 # [('e', 's'), ('es', 't'), ('est', '</w>')]
apply_bpe("lowest", m)            # ['l', 'o', 'w', 'est</w>']
```
''',
"starter": r'''
from collections import Counter


def learn_bpe(word_counts, num_merges):
    # TODO
    return []


def apply_bpe(word, merges):
    # TODO
    return []
''',
"hints": [
    "Keep `vocab = {tuple(w) + ('</w>',): c for w, c in word_counts.items()}`.",
    "Pair counts: for each symbol tuple, add `c` to every `(s[i], s[i+1])`; best = `min(pairs, key=lambda p: (-pairs[p], p))`.",
    "Write `_merge(symbols, pair)` scanning left to right, joining `a + b` when the pair matches.",
],
"solution": r'''
from collections import Counter


def _merge(symbols, pair):
    a, b = pair
    out, i = [], 0
    while i < len(symbols):
        if i + 1 < len(symbols) and symbols[i] == a and symbols[i + 1] == b:
            out.append(a + b)
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def learn_bpe(word_counts, num_merges):
    vocab = {tuple(w) + ("</w>",): c for w, c in word_counts.items()}
    merges = []
    for _ in range(num_merges):
        pairs = Counter()
        for sym, c in vocab.items():
            for i in range(len(sym) - 1):
                pairs[(sym[i], sym[i + 1])] += c
        if not pairs:
            break
        best = min(pairs, key=lambda p: (-pairs[p], p))
        merges.append(best)
        new_vocab = Counter()
        for sym, c in vocab.items():
            new_vocab[_merge(sym, best)] += c
        vocab = dict(new_vocab)
    return merges


def apply_bpe(word, merges):
    sym = tuple(word) + ("</w>",)
    for pair in merges:
        sym = _merge(sym, pair)
    return list(sym)
''',
"explanation": r'''
Each round counts frequency-weighted adjacent pairs, picks the most frequent (smallest on ties),
records it and rewrites every word with a left-to-right, non-overlapping merge. Applying BPE replays
the merges in learned order on a new word.
''',
"tests": r'''
WC = {"low": 5, "lower": 2, "newest": 6, "widest": 3}

class TestBPE(unittest.TestCase):
    def test_first_merges(self):
        self.assertEqual(S.learn_bpe(WC, 3), [("e", "s"), ("es", "t"), ("est", "</w>")])

    def test_apply(self):
        self.assertEqual(S.apply_bpe("lowest", S.learn_bpe(WC, 3)), ["l", "o", "w", "est</w>"])

    def test_more_merges(self):
        m = S.learn_bpe(WC, 5)
        self.assertEqual(m[3:], [("l", "o"), ("lo", "w")])
        self.assertEqual(S.apply_bpe("low", m), ["low", "</w>"])

    def test_no_merges(self):
        self.assertEqual(S.apply_bpe("abc", []), ["a", "b", "c", "</w>"])

    def test_early_stop(self):
        self.assertEqual(S.learn_bpe({"a": 1}, 10), [("a", "</w>")])

    def test_overlap(self):
        self.assertEqual(S.apply_bpe("aaa", [("a", "a")]), ["aa", "a", "</w>"])

    def test_frequency_weighting(self):
        self.assertEqual(S.learn_bpe({"ab": 1, "cd": 5}, 1), [("c", "d")])

    def test_tie_lexicographic(self):
        self.assertEqual(S.learn_bpe({"xy": 1, "ab": 1}, 1), [("a", "b")])
''',
"feedback": [
    ("test_first_merges", "Weight each pair by its word's count and append '</w>' to every word."),
    ("test_overlap", "Merge left to right without overlapping: 'aaa' → 'aa', 'a'."),
    ("test_tie_lexicographic", "On ties choose the smallest pair: min(pairs, key=lambda p: (-count, p))."),
    ("test_apply", "Apply merges in the order they were learned."),
],
},
# ---------------------------------------------------------------- scaled-dot-attention
{
"slug": "scaled-dot-attention", "title": "Scaled Dot-Product Attention",
"difficulty": "intermediate", "prereqs": ["temperature-softmax", "matmul-dot"], "packages": ["numpy"],
"objectives": ["Compute attention scores QKᵀ/√d", "Apply softmax row-wise to get attention weights",
               "Mix value vectors with the weights; support masks"],
"tags": ["attention", "transformers", "softmax", "queries-keys-values"],
"sources": ["S019", "S013"], "entry": "attention(Q, K, V, mask=None)",
"article": r'''
# Scaled Dot-Product Attention

## Intuition
Each token asks a question (query), every token advertises what it contains (key) and what it
would contribute (value). A token's output is a weighted average of all values, weighted by how
well its query matches each key.

## Precise explanation (Vaswani et al., 2017)
For queries $Q$ `(T_q, d_k)`, keys $K$ `(T_k, d_k)`, values $V$ `(T_k, d_v)`:
$$\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.$$
* Scores `(T_q, T_k)`; dividing by $\sqrt{d_k}$ keeps their scale independent of dimension,
  avoiding an overly peaked softmax.
* Softmax is taken over the **key** axis (each row sums to 1).
* A boolean `mask` (True = allowed) sets disallowed scores to −∞ before softmax ([[causal-mask]]).

```mermaid
flowchart LR
  Q --> S["scores = QKᵀ/√d"]
  K --> S
  S --> M[mask] --> W["weights = softmax(rows)"] --> O["output = W V"]
  V --> O
```

## Worked example
Q = [[1, 0]], K = [[1, 0], [0, 1]], V = [[1, 2], [3, 4]], d = 2: scores [0.707, 0] →
weights [0.670, 0.330] → output [1.66, 2.66].

## Common mistakes
* Softmax over the wrong axis.
* Forgetting the √d scaling.
* Masking after softmax (weights no longer sum to 1).

## Why this matters
Attention is the core operation of transformers and LLMs.
''',
"statement": r'''
Write `attention(Q, K, V, mask=None)` returning `(output, weights)`.
* `mask` (optional) is a boolean array broadcastable to `(T_q, T_k)`; False entries get −∞ scores.
* Every query row must have at least one allowed key, else `ValueError`.
* Raise `ValueError` on incompatible shapes.

**Example**
```python
out, w = attention(np.array([[1., 0.]]), np.array([[1., 0.], [0., 1.]]), np.array([[1., 2.], [3., 4.]]))
w     # [[0.6698, 0.3302]]
out   # [[1.6605, 2.6605]]
```
''',
"starter": r'''
import numpy as np


def attention(Q, K, V, mask=None):
    # TODO
    pass
''',
"hints": [
    "`scores = Q @ K.T / np.sqrt(Q.shape[-1])`.",
    "`scores = np.where(mask, scores, -np.inf)`; check `mask.any(axis=1)` for every row.",
    "Stable row softmax, then `weights @ V`.",
],
"solution": r'''
import numpy as np


def attention(Q, K, V, mask=None):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    if Q.ndim != 2 or K.ndim != 2 or V.ndim != 2 or Q.shape[1] != K.shape[1] or K.shape[0] != V.shape[0]:
        raise ValueError("incompatible shapes")
    scores = Q @ K.T / np.sqrt(Q.shape[1])
    if mask is not None:
        m = np.broadcast_to(np.asarray(mask, dtype=bool), scores.shape)
        if not m.any(axis=1).all():
            raise ValueError("a query row has no allowed keys")
        scores = np.where(m, scores, -np.inf)
    scores = scores - scores.max(axis=1, keepdims=True)
    w = np.exp(scores)
    w = w / w.sum(axis=1, keepdims=True)
    return w @ V, w
''',
"explanation": r'''
Scores compare every query with every key, scaled by √d. Masked positions become −∞ so their
softmax weight is exactly 0. A stable row-wise softmax gives attention weights, which mix the value
vectors.
''',
"tests": r'''
import numpy as np

class TestAttention(unittest.TestCase):
    def test_example(self):
        out, w = S.attention(np.array([[1., 0.]]), np.array([[1., 0.], [0., 1.]]), np.array([[1., 2.], [3., 4.]]))
        a = np.exp(1 / np.sqrt(2)); e = np.array([a, 1.0]) / (a + 1)
        np.testing.assert_allclose(w, [e])
        np.testing.assert_allclose(out, [e @ np.array([[1., 2.], [3., 4.]])])

    def test_rows_sum_one(self):
        rng = np.random.default_rng(0)
        _, w = S.attention(rng.normal(size=(4, 8)), rng.normal(size=(6, 8)), rng.normal(size=(6, 3)))
        np.testing.assert_allclose(w.sum(axis=1), 1.0)
        self.assertEqual(w.shape, (4, 6))

    def test_identical_keys_average(self):
        out, _ = S.attention(np.ones((1, 2)), np.ones((3, 2)), np.array([[0.], [3.], [6.]]))
        np.testing.assert_allclose(out, [[3.0]])

    def test_mask(self):
        out, w = S.attention(np.ones((1, 2)), np.ones((2, 2)), np.array([[1.], [5.]]),
                             mask=np.array([[True, False]]))
        np.testing.assert_allclose(w, [[1.0, 0.0]])
        np.testing.assert_allclose(out, [[1.0]])

    def test_scaling(self):
        q = np.array([[2., 2., 2., 2.]]); k = np.array([[1., 1., 1., 1.], [0., 0., 0., 0.]])
        _, w = S.attention(q, k, np.eye(2))
        self.assertAlmostEqual(w[0, 0], 1 / (1 + np.exp(-4.0)))

    def test_all_masked_row(self):
        with self.assertRaises(ValueError):
            S.attention(np.ones((1, 2)), np.ones((2, 2)), np.ones((2, 1)), mask=np.array([[False, False]]))

    def test_shape_error(self):
        with self.assertRaises(ValueError):
            S.attention(np.ones((1, 3)), np.ones((2, 2)), np.ones((2, 1)))
''',
"feedback": [
    ("test_scaling", "Divide scores by sqrt(d_k)."),
    ("test_rows_sum_one", "Softmax over the key axis (axis=1)."),
    ("test_mask", "Set disallowed scores to −inf *before* softmax."),
    ("test_all_masked_row", "Raise ValueError if a query has no allowed keys."),
],
},
# ---------------------------------------------------------------- causal-mask
{
"slug": "causal-mask", "title": "Causal Masking",
"difficulty": "intermediate", "prereqs": ["scaled-dot-attention"], "packages": ["numpy"],
"objectives": ["Build a lower-triangular causal mask", "Combine causal and padding masks",
               "Verify that outputs do not depend on future tokens"],
"tags": ["causal-mask", "padding-mask", "autoregressive", "attention"],
"sources": ["S019", "S013"], "entry": "causal_mask(T); padding_mask(lengths, T); combined_mask(lengths, T)",
"article": r'''
# Causal and Padding Masks

## Intuition
A language model predicting token t must not peek at tokens after t. The **causal mask** hides the
future: position t may attend only to positions 0..t. A **padding mask** hides filler tokens added to
make sequences in a batch the same length.

## Precise explanation
* Causal mask `M[i, j] = (j <= i)` — lower triangle including the diagonal:
  `np.tril(np.ones((T, T), bool))`.
* Padding mask for a batch with true lengths $L_b$: key position j is valid iff $j < L_b$, shape
  `(B, T)`; broadcast as `(B, 1, T)` over queries.
* Combined `(B, T, T)` = causal AND padding.
With masked scores set to −∞, changing a future token cannot change earlier outputs — testable!

|   | k0 | k1 | k2 |
|---|---|---|---|
| q0 | ✓ | ✗ | ✗ |
| q1 | ✓ | ✓ | ✗ |
| q2 | ✓ | ✓ | ✓ |

## Worked example
T = 3 → [[T, F, F], [T, T, F], [T, T, T]]; lengths [2] → padding [[T, T, F]].

## Common mistakes
* Upper instead of lower triangle (attending only to the future).
* Excluding the diagonal (a token can attend to itself).
* Rows of padding queries that become fully masked under both masks — we keep the causal diagonal
  so every row has at least one allowed key.

## Why this matters
Causal masking is what makes decoder-only transformers (GPT-style) autoregressive and enables
training on all positions of a sequence in parallel.
''',
"statement": r'''
Implement:
* `causal_mask(T)` → bool `(T, T)` lower triangle with diagonal. `T >= 1` else `ValueError`.
* `padding_mask(lengths, T)` → bool `(B, T)`, True for `j < lengths[b]`; each length in `1..T`.
* `combined_mask(lengths, T)` → bool `(B, T, T)` = causal AND padding-over-keys, **but** with the
  diagonal always True (so padded query rows still have one allowed key).

**Examples**
```python
causal_mask(3)              # [[T,F,F],[T,T,F],[T,T,T]]
padding_mask([2, 3], 3)     # [[T,T,F],[T,T,T]]
combined_mask([2], 3)[0]    # [[T,F,F],[T,T,F],[T,T,T]]  — row 2's own diagonal kept
```
''',
"starter": r'''
import numpy as np


def causal_mask(T):
    pass


def padding_mask(lengths, T):
    pass


def combined_mask(lengths, T):
    pass
''',
"hints": [
    "`np.tril(np.ones((T, T), dtype=bool))`.",
    "`np.arange(T)[None, :] < np.asarray(lengths)[:, None]`.",
    "`causal[None] & pad[:, None, :]`, then OR with `np.eye(T, dtype=bool)`.",
],
"solution": r'''
import numpy as np


def causal_mask(T):
    if T < 1:
        raise ValueError("T must be >= 1")
    return np.tril(np.ones((T, T), dtype=bool))


def padding_mask(lengths, T):
    L = np.asarray(lengths)
    if L.ndim != 1 or (L < 1).any() or (L > T).any():
        raise ValueError("lengths must be in 1..T")
    return np.arange(T)[None, :] < L[:, None]


def combined_mask(lengths, T):
    m = causal_mask(T)[None, :, :] & padding_mask(lengths, T)[:, None, :]
    return m | np.eye(T, dtype=bool)[None, :, :]
''',
"explanation": r'''
`tril` builds the causal pattern; comparing positions with lengths builds padding masks by
broadcasting. Their conjunction over keys, plus the diagonal, gives a per-sequence mask in which
every query has at least one allowed key.
''',
"tests": r'''
import numpy as np

T_, F_ = True, False

def attn(Q, K, V, mask):
    s = Q @ K.T / np.sqrt(Q.shape[1]); s = np.where(mask, s, -np.inf)
    w = np.exp(s - s.max(1, keepdims=True)); w /= w.sum(1, keepdims=True); return w @ V

class TestMasks(unittest.TestCase):
    def test_causal(self):
        np.testing.assert_array_equal(S.causal_mask(3), [[T_, F_, F_], [T_, T_, F_], [T_, T_, T_]])

    def test_padding(self):
        np.testing.assert_array_equal(S.padding_mask([2, 3], 3), [[T_, T_, F_], [T_, T_, T_]])

    def test_combined(self):
        np.testing.assert_array_equal(S.combined_mask([2], 3)[0], [[T_, F_, F_], [T_, T_, F_], [T_, T_, T_]])
        np.testing.assert_array_equal(S.combined_mask([1], 3)[0], [[T_, F_, F_], [T_, T_, F_], [T_, F_, T_]])

    def test_combined_shape(self):
        self.assertEqual(S.combined_mask([1, 2, 4], 4).shape, (3, 4, 4))

    def test_no_future_leak(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(5, 4)); M = S.causal_mask(5)
        out1 = attn(X, X, X, M)
        X2 = X.copy(); X2[4] += 10.0
        out2 = attn(X2, X2, X2, M)
        np.testing.assert_allclose(out1[:4], out2[:4])

    def test_every_row_has_key(self):
        self.assertTrue(S.combined_mask([1, 3], 3).any(axis=2).all())

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.causal_mask(0)
        with self.assertRaises(ValueError):
            S.padding_mask([4], 3)
''',
"feedback": [
    ("test_causal", "Use the lower triangle including the diagonal (np.tril)."),
    ("test_padding", "Key j is valid iff j < length."),
    ("test_combined", "AND the masks over keys, then OR with the identity so the diagonal stays True."),
    ("test_no_future_leak", "With a correct causal mask, changing the last token leaves earlier outputs unchanged."),
],
},
# ---------------------------------------------------------------- positional-encoding
{
"slug": "positional-encoding", "title": "Sinusoidal Positional Encoding",
"difficulty": "intermediate", "prereqs": ["scaled-dot-attention"], "packages": ["numpy"],
"objectives": ["Implement the sinusoidal encoding from the Transformer paper",
               "Explain why attention needs positional information", "Check bounded values and relative-position structure"],
"tags": ["positional-encoding", "transformers", "sinusoids"],
"sources": ["S019", "S013"], "entry": "positional_encoding(T, d)",
"article": r'''
# Sinusoidal Positional Encoding

## Intuition
Attention treats its inputs as a *set*: shuffle the tokens and each output is just shuffled too.
To know word order, we add a position-dependent vector to each token embedding.

## Precise explanation (Vaswani et al., 2017)
For position $p$ and dimension index $i$ (with $d$ even):
$$PE[p, 2i] = \sin\!\left(\frac{p}{10000^{2i/d}}\right),\qquad PE[p, 2i+1] = \cos\!\left(\frac{p}{10000^{2i/d}}\right).$$
Each pair of dimensions is a sine/cosine at a different frequency, from fast (i = 0) to very slow.
Values lie in [−1, 1]. For any offset k, $PE[p+k]$ is a fixed linear function (a rotation per
frequency pair) of $PE[p]$, which helps attention reason about relative positions. Many modern LLMs
use learned or rotary (RoPE) encodings instead; the sinusoidal version is the classic starting point.

## Worked example
p = 0: all sines 0, all cosines 1 → [0, 1, 0, 1, …]. p = 1, d = 4: frequencies 1 and 1/100 →
[sin 1, cos 1, sin 0.01, cos 0.01] = [0.841, 0.540, 0.010, 1.000].

## Common mistakes
* Using $i$ instead of $2i$ in the exponent.
* Interleaving incorrectly (sin on odd dimensions).
* Integer division producing zeros.

## Why this matters
Without positional information "dog bites man" and "man bites dog" look identical to a transformer.
''',
"statement": r'''
Write `positional_encoding(T, d)` returning a float array `(T, d)` per the formula (positions
`0..T-1`). Raise `ValueError` if `T < 1`, `d < 2`, or `d` is odd. No Python loops over positions are
required (vectorise if you can).

**Example**
```python
pe = positional_encoding(2, 4)
pe[0]   # [0., 1., 0., 1.]
pe[1]   # [0.84147, 0.54030, 0.01000, 0.99995]
```
''',
"starter": r'''
import numpy as np


def positional_encoding(T, d):
    pass
''',
"hints": [
    "`pos = np.arange(T)[:, None]`; `i = np.arange(d // 2)[None, :]`.",
    "`angles = pos / 10000 ** (2 * i / d)`.",
    "`pe[:, 0::2] = np.sin(angles)`; `pe[:, 1::2] = np.cos(angles)`.",
],
"solution": r'''
import numpy as np


def positional_encoding(T, d):
    if T < 1 or d < 2 or d % 2:
        raise ValueError("T >= 1 and even d >= 2 required")
    pos = np.arange(T)[:, None]
    i = np.arange(d // 2)[None, :]
    angles = pos / np.power(10000.0, 2 * i / d)
    pe = np.zeros((T, d))
    pe[:, 0::2] = np.sin(angles)
    pe[:, 1::2] = np.cos(angles)
    return pe
''',
"explanation": r'''
A `(T, d/2)` grid of angles is built by broadcasting positions against frequencies; sines fill even
columns and cosines odd columns.
''',
"tests": r'''
import numpy as np

class TestPE(unittest.TestCase):
    def test_pos0(self):
        np.testing.assert_allclose(S.positional_encoding(1, 6)[0], [0, 1, 0, 1, 0, 1])

    def test_pos1(self):
        np.testing.assert_allclose(S.positional_encoding(2, 4)[1],
                                   [np.sin(1), np.cos(1), np.sin(0.01), np.cos(0.01)])

    def test_shape_bounds(self):
        pe = S.positional_encoding(50, 16)
        self.assertEqual(pe.shape, (50, 16))
        self.assertTrue((np.abs(pe) <= 1).all())

    def test_pair_norm(self):
        pe = S.positional_encoding(20, 8)
        np.testing.assert_allclose(pe[:, 0::2] ** 2 + pe[:, 1::2] ** 2, 1.0)

    def test_relative_rotation(self):
        pe = S.positional_encoding(30, 8); k = 3
        w = 1 / 10000 ** (2 * np.arange(4) / 8)
        for j in range(4):
            c, s = np.cos(k * w[j]), np.sin(k * w[j])
            R = np.array([[c, -s], [s, c]])
            for p in range(25):
                np.testing.assert_allclose(pe[p, 2*j:2*j+2] @ R, pe[p + k, 2*j:2*j+2], atol=1e-10)

    def test_distinct_positions(self):
        pe = S.positional_encoding(100, 32)
        self.assertEqual(len({tuple(np.round(r, 8)) for r in pe}), 100)

    def test_errors(self):
        for T, d in [(0, 4), (3, 5), (3, 0)]:
            with self.assertRaises(ValueError):
                S.positional_encoding(T, d)
''',
"feedback": [
    ("test_pos1", "Exponent is 2i/d with i indexing dimension *pairs*."),
    ("test_pos0", "Sines go in even columns, cosines in odd columns."),
    ("test_relative_rotation", "Use the exact frequencies 1/10000^(2i/d)."),
    ("test_errors", "Reject odd d."),
],
},
# ---------------------------------------------------------------- top-k-top-p
{
"slug": "top-k-top-p", "title": "Top-k and Top-p Filtering",
"difficulty": "advanced", "prereqs": ["temperature-softmax"], "packages": ["numpy"],
"objectives": ["Restrict sampling to the top-k tokens", "Implement nucleus (top-p) filtering",
               "Sample deterministically from a distribution with inverse-CDF"],
"tags": ["sampling", "top-k", "top-p", "nucleus-sampling", "decoding"],
"sources": ["S021", "S022"], "entry": "top_k_filter(p, k); top_p_filter(p, top_p); sample(p, u)",
"article": r'''
# Top-k and Nucleus Sampling

## Intuition
Sampling from the full distribution occasionally picks absurd low-probability tokens. Truncating to
the most likely candidates keeps diversity while cutting off the unreliable tail.

## Precise explanation
* **Top-k:** keep the k most probable tokens (ties → lower index), zero the rest, renormalise.
* **Top-p (nucleus; Holtzman et al., 2019):** sort probabilities descending and keep the smallest
  prefix whose cumulative probability is **≥ p**; renormalise. The nucleus adapts: small when the
  model is confident, large when it is unsure. Always keep at least one token.
* **Sampling with a uniform number u ∈ [0, 1):** return the first index whose cumulative probability
  exceeds u (inverse CDF). Passing u explicitly makes tests deterministic; in practice
  `u = rng.random()`.

## Worked example
p = [0.5, 0.2, 0.15, 0.1, 0.05]; top-k 2 → [0.714, 0.286, 0, 0, 0]. top-p 0.8 → cumulative
0.5, 0.7, 0.85 ≥ 0.8 → keep 3 → [0.588, 0.235, 0.176, 0, 0]. sample(u = 0.6) on the original p → index 1
(cumulative 0.5 ≤ 0.6 < 0.7).

## Common mistakes
* Forgetting to renormalise.
* Off-by-one in top-p: include the token that crosses the threshold.
* Sorting and then returning probabilities in sorted order (they must stay aligned with the vocabulary).

## Why this matters
Top-k, top-p and temperature ([[temperature-softmax]]) are the knobs exposed by LLM APIs and libraries.
''',
"statement": r'''
For a 1-D probability array `p` (non-negative, sums to 1):
* `top_k_filter(p, k)` → renormalised array keeping the k largest (ties → lower index);
  `1 <= k <= len(p)` else `ValueError`.
* `top_p_filter(p, top_p)` → renormalised nucleus; `0 < top_p <= 1` else `ValueError`.
* `sample(p, u)` → int index: first i with `cumsum(p)[i] > u`, for `0 <= u < 1` (if rounding leaves
  no such i, return the last index with `p > 0`).

**Examples**
```python
p = np.array([0.5, 0.2, 0.15, 0.1, 0.05])
top_k_filter(p, 2)     # [0.7143, 0.2857, 0, 0, 0]
top_p_filter(p, 0.8)   # [0.5882, 0.2353, 0.1765, 0, 0]
sample(p, 0.6)         # 1
```
''',
"starter": r'''
import numpy as np


def top_k_filter(p, k):
    pass


def top_p_filter(p, top_p):
    pass


def sample(p, u):
    pass
''',
"hints": [
    "`order = np.argsort(-p, kind='stable')`; keep `order[:k]`.",
    "For top-p: `c = np.cumsum(p[order])`; `n_keep = int(np.searchsorted(c, top_p) + 1)` (cap at len).",
    "Sampling: `np.searchsorted(np.cumsum(p), u, side='right')`.",
],
"solution": r'''
import numpy as np


def _keep(p, idx):
    out = np.zeros_like(p)
    out[idx] = p[idx]
    return out / out.sum()


def top_k_filter(p, k):
    p = np.asarray(p, dtype=float)
    if not 1 <= k <= len(p):
        raise ValueError("k out of range")
    return _keep(p, np.argsort(-p, kind="stable")[:k])


def top_p_filter(p, top_p):
    p = np.asarray(p, dtype=float)
    if not 0 < top_p <= 1:
        raise ValueError("top_p must be in (0, 1]")
    order = np.argsort(-p, kind="stable")
    c = np.cumsum(p[order])
    n_keep = min(int(np.searchsorted(c, top_p - 1e-12)) + 1, len(p))
    return _keep(p, order[:n_keep])


def sample(p, u):
    p = np.asarray(p, dtype=float)
    if not 0 <= u < 1:
        raise ValueError("u must be in [0, 1)")
    i = int(np.searchsorted(np.cumsum(p), u, side="right"))
    if i >= len(p):
        i = int(np.flatnonzero(p > 0)[-1])
    return i
''',
"explanation": r'''
A stable descending argsort gives the ranking. Top-k keeps a fixed prefix; top-p finds the first
prefix whose cumulative mass reaches the threshold (a tiny tolerance absorbs rounding such as
0.5 + 0.2 + 0.15 being slightly below 0.85) and keeps it. Both renormalise in vocabulary order.
Sampling inverts the CDF with `searchsorted`.
''',
"tests": r'''
import numpy as np

P = np.array([0.5, 0.2, 0.15, 0.1, 0.05])

class TestSampling(unittest.TestCase):
    def test_top_k(self):
        np.testing.assert_allclose(S.top_k_filter(P, 2), [0.5 / 0.7, 0.2 / 0.7, 0, 0, 0])

    def test_top_k_ties(self):
        np.testing.assert_allclose(S.top_k_filter(np.array([0.25, 0.25, 0.5]), 2), [1 / 3, 0, 2 / 3])

    def test_top_p(self):
        np.testing.assert_allclose(S.top_p_filter(P, 0.8), [0.5 / 0.85, 0.2 / 0.85, 0.15 / 0.85, 0, 0])

    def test_top_p_exact_boundary(self):
        np.testing.assert_allclose(S.top_p_filter(P, 0.7), [0.5 / 0.7, 0.2 / 0.7, 0, 0, 0])

    def test_top_p_keeps_one(self):
        np.testing.assert_allclose(S.top_p_filter(P, 0.01), [1, 0, 0, 0, 0])

    def test_top_p_full(self):
        np.testing.assert_allclose(S.top_p_filter(P, 1.0), P)

    def test_order_preserved(self):
        p = np.array([0.1, 0.6, 0.3])
        np.testing.assert_allclose(S.top_k_filter(p, 2), [0, 2 / 3, 1 / 3])

    def test_sample(self):
        self.assertEqual(S.sample(P, 0.6), 1)
        self.assertEqual(S.sample(P, 0.0), 0)
        self.assertEqual(S.sample(P, 0.999), 4)
        self.assertEqual(S.sample(S.top_k_filter(P, 1), 0.99), 0)

    def test_sample_frequencies(self):
        rng = np.random.default_rng(0)
        draws = np.bincount([S.sample(P, rng.random()) for _ in range(20000)], minlength=5) / 20000
        np.testing.assert_allclose(draws, P, atol=0.015)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.top_k_filter(P, 0)
        with self.assertRaises(ValueError):
            S.top_p_filter(P, 0)
''',
"feedback": [
    ("test_top_p", "Keep the smallest prefix whose cumulative probability is >= top_p (include the crossing token)."),
    ("test_top_p_exact_boundary", "Floating-point sums like 0.5+0.2 may be 0.7000000000000001; use a tiny tolerance."),
    ("test_order_preserved", "Return probabilities in original vocabulary order."),
    ("test_sample", "Return the first index whose cumulative probability is > u."),
],
},
# ---------------------------------------------------------------- multi-head-attention
{
"slug": "multi-head-attention", "title": "Multi-Head Attention",
"difficulty": "intermediate", "prereqs": ["scaled-dot-attention", "causal-mask"], "packages": ["numpy"],
"objectives": ["Project inputs to queries, keys and values", "Split into heads, attend in parallel and concatenate",
               "Apply the output projection and optional causal mask"],
"tags": ["multi-head-attention", "transformers", "reshaping", "self-attention"],
"sources": ["S019", "S013"], "entry": "split_heads(X, h); merge_heads(Xh); multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal=False)",
"article": r'''
# Multi-Head Self-Attention

## Intuition
One attention pattern can focus on one kind of relationship. Multiple heads let the model attend to
different things at once — syntax in one head, coreference in another — then combine the results.

## Precise explanation
For input $X$ `(T, d_model)` and $h$ heads with $d_h = d_\text{model}/h$:
1. $Q = XW_q,\ K = XW_k,\ V = XW_v$ (each `(T, d_model)`).
2. **Split heads:** reshape `(T, d_model)` → `(T, h, d_h)` → transpose to `(h, T, d_h)`.
3. Per head: $\text{softmax}(Q_iK_i^\top/\sqrt{d_h} + \text{mask})V_i$.
4. **Merge heads:** `(h, T, d_h)` → `(T, h, d_h)` → `(T, d_model)` (concatenation).
5. Output projection: $\text{concat}\cdot W_o$.
With h = 1 this reduces to single-head attention followed by $W_o$.

```mermaid
flowchart LR
  X --> Q["XWq"] & K["XWk"] & V["XWv"]
  Q & K & V --> SH["split into h heads"] --> A["attention per head"] --> MH["concat heads"] --> O["· Wo"]
```

## Worked example
d_model = 4, h = 2: head 0 uses feature columns 0–1 of Q/K/V, head 1 columns 2–3.

## Common mistakes
* Reshaping `(T, d)` to `(h, T, d_h)` directly (mixes positions and features) — reshape then transpose.
* Scaling by √d_model instead of √d_h.
* Forgetting the output projection.

## Why this matters
This block (plus a feed-forward layer and residual connections) is the transformer layer stacked
dozens of times in every LLM.
''',
"statement": r'''
Implement:
* `split_heads(X, h)` → `(h, T, d/h)`; raise `ValueError` if `d % h != 0`.
* `merge_heads(Xh)` → inverse of `split_heads`.
* `multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal=False)` → `(T, d_model)` output following the
  steps above (causal mask from [[causal-mask]] when `causal=True`).

All weight matrices are `(d_model, d_model)`.

**Example**
```python
X = np.arange(8.).reshape(2, 4)
split_heads(X, 2)[1]       # [[2., 3.], [6., 7.]]
merge_heads(split_heads(X, 2))   # equals X
```
''',
"starter": r'''
import numpy as np


def split_heads(X, h):
    pass


def merge_heads(Xh):
    pass


def multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal=False):
    pass
''',
"hints": [
    "`X.reshape(T, h, d // h).transpose(1, 0, 2)`.",
    "Merge: `Xh.transpose(1, 0, 2).reshape(T, h * dh)`.",
    "Batched scores: `Qh @ Kh.transpose(0, 2, 1) / np.sqrt(dh)` → shape `(h, T, T)`.",
],
"solution": r'''
import numpy as np


def split_heads(X, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    if h < 1 or d % h:
        raise ValueError("d_model must be divisible by h")
    return X.reshape(T, h, d // h).transpose(1, 0, 2)


def merge_heads(Xh):
    h, T, dh = Xh.shape
    return Xh.transpose(1, 0, 2).reshape(T, h * dh)


def multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal=False):
    X = np.asarray(X, dtype=float)
    Qh, Kh, Vh = (split_heads(X @ W, h) for W in (Wq, Wk, Wv))
    dh = Qh.shape[-1]
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(dh)
    if causal:
        T = X.shape[0]
        scores = np.where(np.tril(np.ones((T, T), dtype=bool))[None], scores, -np.inf)
    scores = scores - scores.max(axis=-1, keepdims=True)
    w = np.exp(scores)
    w = w / w.sum(axis=-1, keepdims=True)
    return merge_heads(w @ Vh) @ Wo
''',
"explanation": r'''
Reshape-then-transpose keeps each position's features together while grouping them by head.
Batched matrix products compute all heads' attention at once; merging reverses the split and the
output projection mixes information across heads.
''',
"tests": r'''
import numpy as np

def single_head(Q, K, V, causal=False):
    s = Q @ K.T / np.sqrt(Q.shape[1])
    if causal:
        s = np.where(np.tril(np.ones(s.shape, bool)), s, -np.inf)
    w = np.exp(s - s.max(1, keepdims=True)); w /= w.sum(1, keepdims=True)
    return w @ V

class TestMHA(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(0)
        self.X = rng.normal(size=(5, 8))
        self.W = [rng.normal(size=(8, 8)) / 3 for _ in range(4)]

    def test_split(self):
        X = np.arange(8.).reshape(2, 4)
        np.testing.assert_array_equal(S.split_heads(X, 2)[1], [[2., 3.], [6., 7.]])
        self.assertEqual(S.split_heads(X, 2).shape, (2, 2, 2))

    def test_roundtrip(self):
        np.testing.assert_array_equal(S.merge_heads(S.split_heads(self.X, 4)), self.X)

    def test_h1_equals_single(self):
        Wq, Wk, Wv, Wo = self.W
        exp = single_head(self.X @ Wq, self.X @ Wk, self.X @ Wv) @ Wo
        np.testing.assert_allclose(S.multi_head_attention(self.X, Wq, Wk, Wv, Wo, 1), exp)

    def test_h2_manual(self):
        Wq, Wk, Wv, Wo = self.W
        Q, K, V = self.X @ Wq, self.X @ Wk, self.X @ Wv
        heads = [single_head(Q[:, i*4:(i+1)*4], K[:, i*4:(i+1)*4], V[:, i*4:(i+1)*4]) for i in range(2)]
        np.testing.assert_allclose(S.multi_head_attention(self.X, Wq, Wk, Wv, Wo, 2), np.hstack(heads) @ Wo)

    def test_causal(self):
        Wq, Wk, Wv, Wo = self.W
        out = S.multi_head_attention(self.X, Wq, Wk, Wv, Wo, 2, causal=True)
        X2 = self.X.copy(); X2[-1] += 5
        out2 = S.multi_head_attention(X2, Wq, Wk, Wv, Wo, 2, causal=True)
        np.testing.assert_allclose(out[:-1], out2[:-1])

    def test_shape(self):
        self.assertEqual(S.multi_head_attention(self.X, *self.W, h=4).shape, (5, 8))

    def test_bad_heads(self):
        with self.assertRaises(ValueError):
            S.split_heads(self.X, 3)
''',
"feedback": [
    ("test_split", "Reshape to (T, h, d_h) and then transpose to (h, T, d_h)."),
    ("test_h2_manual", "Scale each head's scores by sqrt(d_h), not sqrt(d_model)."),
    ("test_h1_equals_single", "Remember the output projection Wo."),
    ("test_causal", "Apply the causal mask to every head's scores."),
],
},
# ---------------------------------------------------------------- beam-search
{
"slug": "beam-search", "title": "Beam Search",
"difficulty": "advanced", "prereqs": ["greedy-decoding"], "packages": ["numpy"],
"objectives": ["Keep the B best partial sequences by total log-probability",
               "Handle finished hypotheses (EOS)", "See why beam search can beat greedy decoding"],
"tags": ["beam-search", "decoding", "log-probabilities", "search"],
"sources": ["S013", "S022"], "entry": "beam_search(next_logprobs, prompt, vocab, beam_width=2, max_new=5, eos='</s>')",
"article": r'''
# Beam Search

## Intuition
Greedy decoding commits to the best next token even if it leads into a poor continuation. Beam search
keeps the B most promising partial sentences at every step, so a slightly worse first word can still
win if it leads to a much better whole sentence.

## Precise explanation
Score of a sequence = sum of the log-probabilities of its generated tokens.
```text
beams = [(prompt, 0.0)]
repeat max_new times:
    candidates = []
    for (seq, score) in beams:
        if seq ends with EOS: keep (seq, score) as a candidate unchanged
        else: for every token t: candidates.append((seq + [t], score + logp(t | seq)))
    beams = best B candidates (ties: lexicographically smaller token list)
    stop early if all beams end with EOS
return the best beam
```
B = 1 is greedy decoding. Without length normalisation, beam search prefers shorter outputs because
every token adds a negative log-probability — real systems often divide by length^α.

## Worked example
Step 1: P(a) = 0.6, P(b) = 0.4. After a: best next 0.4; after b: best next 0.9.
Greedy: a → 0.6·0.4 = 0.24. Beam (B = 2): b → 0.4·0.9 = 0.36 — better.

## Common mistakes
* Multiplying probabilities (underflow) instead of adding log-probabilities.
* Expanding finished hypotheses past EOS.
* Comparing beams of different lengths without considering the length bias.

## Why this matters
Beam search is standard in machine translation, speech recognition and constrained generation.
''',
"statement": r'''
Write `beam_search(next_logprobs, prompt, vocab, beam_width=2, max_new=5, eos="</s>")` returning
`(best_tokens, best_score)`. `next_logprobs(tokens)` returns a 1-D array of log-probabilities aligned
with `vocab`. Follow the pseudocode exactly (ties → lexicographically smaller token list). Raise
`ValueError` if `beam_width < 1` or `max_new < 1`.

**Example**
```python
vocab = ["a", "b", "</s>"]
def f(t):
    last = t[-1]
    table = {"<s>": [0.6, 0.4, 1e-9], "a": [0.3, 0.3, 0.4], "b": [0.05, 0.05, 0.9]}
    return np.log(np.array(table.get(last, [1e-9, 1e-9, 1.0])))
beam_search(f, ["<s>"], vocab, beam_width=2, max_new=3)
# (['<s>', 'b', '</s>'], log(0.36))
```
''',
"starter": r'''
import numpy as np


def beam_search(next_logprobs, prompt, vocab, beam_width=2, max_new=5, eos="</s>"):
    # TODO
    pass
''',
"hints": [
    "Store beams as `(tokens_list, score)`; finished beams are carried over unchanged.",
    "Sort candidates with `key=lambda c: (-c[1], c[0])` and keep `[:beam_width]`.",
    "Break when every beam's last token is `eos`.",
],
"solution": r'''
import numpy as np


def beam_search(next_logprobs, prompt, vocab, beam_width=2, max_new=5, eos="</s>"):
    if beam_width < 1 or max_new < 1:
        raise ValueError("beam_width and max_new must be >= 1")
    beams = [(list(prompt), 0.0)]
    for _ in range(max_new):
        candidates = []
        for seq, score in beams:
            if seq and seq[-1] == eos:
                candidates.append((seq, score))
                continue
            lp = np.asarray(next_logprobs(seq), dtype=float)
            for t, l in zip(vocab, lp):
                candidates.append((seq + [t], score + float(l)))
        candidates.sort(key=lambda c: (-c[1], c[0]))
        beams = candidates[:beam_width]
        if all(seq and seq[-1] == eos for seq, _ in beams):
            break
    return beams[0][0], beams[0][1]
''',
"explanation": r'''
Each step expands every unfinished beam by every token, adds log-probabilities, carries finished
beams forward, and keeps the top B by score with a deterministic tie-break. The loop ends at the
length limit or when every surviving beam has produced EOS.
''',
"tests": r'''
import numpy as np

VOCAB = ["a", "b", "</s>"]
TABLE = {"<s>": [0.6, 0.4, 1e-9], "a": [0.3, 0.3, 0.4], "b": [0.05, 0.05, 0.9]}
def F(t):
    return np.log(np.array(TABLE.get(t[-1], [1e-9, 1e-9, 1.0])))

class TestBeam(unittest.TestCase):
    def test_beats_greedy(self):
        toks, score = S.beam_search(F, ["<s>"], VOCAB, beam_width=2, max_new=3)
        self.assertEqual(toks, ["<s>", "b", "</s>"])
        self.assertAlmostEqual(score, np.log(0.36))

    def test_width1_is_greedy(self):
        toks, score = S.beam_search(F, ["<s>"], VOCAB, beam_width=1, max_new=3)
        self.assertEqual(toks, ["<s>", "a", "</s>"])
        self.assertAlmostEqual(score, np.log(0.24))

    def test_max_new_limit(self):
        toks, _ = S.beam_search(F, ["<s>"], VOCAB, beam_width=2, max_new=1)
        self.assertEqual(toks, ["<s>", "a"])

    def test_finished_not_extended(self):
        calls = []
        def f(t):
            calls.append(tuple(t)); return F(t)
        S.beam_search(f, ["<s>"], VOCAB, beam_width=2, max_new=5)
        self.assertFalse(any(c[-1] == "</s>" for c in calls))

    def test_tie_break(self):
        g = lambda t: np.log(np.array([0.5, 0.5, 1e-12])) if len(t) == 1 else np.log(np.array([1e-12, 1e-12, 1.0]))
        toks, _ = S.beam_search(g, ["<s>"], VOCAB, beam_width=1, max_new=2)
        self.assertEqual(toks, ["<s>", "a", "</s>"])

    def test_score_is_sum_logprobs(self):
        toks, score = S.beam_search(F, ["<s>"], VOCAB, beam_width=3, max_new=2)
        exp = sum(F(toks[:i])[VOCAB.index(toks[i])] for i in range(1, len(toks)))
        self.assertAlmostEqual(score, exp)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.beam_search(F, ["<s>"], VOCAB, beam_width=0)
''',
"feedback": [
    ("test_beats_greedy", "Keep the top beam_width candidates by summed log-probability."),
    ("test_finished_not_extended", "Carry finished (EOS) beams forward without calling the model."),
    ("test_tie_break", "Sort with key (-score, tokens) for deterministic ties."),
    ("test_max_new_limit", "Stop after max_new expansion steps."),
],
},
# ---------------------------------------------------------------- kv-cache
{
"slug": "kv-cache", "title": "Incremental Decoding with a KV Cache",
"difficulty": "advanced", "prereqs": ["causal-mask", "multi-head-attention"], "packages": ["numpy"],
"objectives": ["Cache keys and values of past tokens", "Compute attention for one new token at a time",
               "Prove the cached result equals full causal attention"],
"tags": ["kv-cache", "inference", "efficiency", "causal-attention"],
"sources": ["S019", "S022"], "entry": "class KVCache(Wq, Wk, Wv): step(x_t); full_causal_attention(X, Wq, Wk, Wv)",
"article": r'''
# The KV Cache

## Intuition
When generating token 100, a naive loop recomputes keys and values for tokens 1–99 — which haven't
changed. Store them once and only compute the new token's query, key and value each step.

## Precise explanation
With causal attention, the output at position t depends only on $q_t$ and $k_{0..t}, v_{0..t}$.
Each step:
1. $q_t = x_tW_q$, $k_t = x_tW_k$, $v_t = x_tW_v$.
2. Append $k_t, v_t$ to the cache (shapes grow `(t+1, d)`).
3. $o_t = \text{softmax}(q_tK^\top/\sqrt d)\,V$ using all cached rows.
Total work for T steps drops from $O(T^3)$-ish recomputation to $O(T^2)$, at the cost of memory
that grows linearly with context length — the reason long-context LLM serving is memory-bound.
Correctness check: stacking the $o_t$ must equal full causal attention over the whole sequence.

## Worked example
After 3 steps the cache holds 3 key rows and 3 value rows; step 4 computes 1 query, 1 key, 1 value
and attends over 4 rows.

## Common mistakes
* Recomputing keys of old tokens with new weights or new inputs.
* Forgetting the √d scale.
* Letting the new token attend only to the past (it must include itself).

## Why this matters
KV caching is a core optimisation in LLM inference servers.
''',
"statement": r'''
Implement single-head attention (weights `(d, d)`):
* `full_causal_attention(X, Wq, Wk, Wv)` → `(T, d)` outputs with a causal mask.
* `class KVCache(Wq, Wk, Wv)` with attributes `K` and `V` (arrays with 0 rows initially, shape
  `(0, d)`) and `step(x_t)` taking one token vector `(d,)`, appending its key/value and returning its
  output `(d,)`.

**Example**
```python
cache = KVCache(Wq, Wk, Wv)
outs = np.array([cache.step(x) for x in X])
np.allclose(outs, full_causal_attention(X, Wq, Wk, Wv))   # True
cache.K.shape   # (len(X), d)
```
''',
"starter": r'''
import numpy as np


def full_causal_attention(X, Wq, Wk, Wv):
    pass


class KVCache:
    def __init__(self, Wq, Wk, Wv):
        # TODO
        pass

    def step(self, x_t):
        # TODO
        pass
''',
"hints": [
    "Full: scores `Q @ K.T / sqrt(d)`, mask with `np.tril`, softmax rows, multiply V.",
    "Cache init: `self.K = np.zeros((0, d))`; append with `np.vstack([self.K, k_t])`.",
    "Step: `s = self.K @ q_t / sqrt(d)`; softmax over s; `w @ self.V`.",
],
"solution": r'''
import numpy as np


def _softmax(s, axis=-1):
    s = s - s.max(axis=axis, keepdims=True)
    e = np.exp(s)
    return e / e.sum(axis=axis, keepdims=True)


def full_causal_attention(X, Wq, Wk, Wv):
    X = np.asarray(X, dtype=float)
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    T, d = Q.shape
    s = Q @ K.T / np.sqrt(d)
    s = np.where(np.tril(np.ones((T, T), dtype=bool)), s, -np.inf)
    return _softmax(s, axis=1) @ V


class KVCache:
    def __init__(self, Wq, Wk, Wv):
        self.Wq = np.asarray(Wq, dtype=float)
        self.Wk = np.asarray(Wk, dtype=float)
        self.Wv = np.asarray(Wv, dtype=float)
        d = self.Wk.shape[1]
        self.K = np.zeros((0, d))
        self.V = np.zeros((0, self.Wv.shape[1]))

    def step(self, x_t):
        x_t = np.asarray(x_t, dtype=float)
        q, k, v = x_t @ self.Wq, x_t @ self.Wk, x_t @ self.Wv
        self.K = np.vstack([self.K, k])
        self.V = np.vstack([self.V, v])
        w = _softmax(self.K @ q / np.sqrt(q.shape[0]))
        return w @ self.V
''',
"explanation": r'''
The full version builds all queries, keys and values and masks the future. The cached version
computes projections only for the new token, appends its key and value, and attends over every
cached row — exactly the keys a causal mask would allow — so both give identical outputs.
''',
"tests": r'''
import numpy as np

class TestKVCache(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(0)
        self.X = rng.normal(size=(7, 4))
        self.W = [rng.normal(size=(4, 4)) for _ in range(3)]

    def test_matches_full(self):
        cache = S.KVCache(*self.W)
        outs = np.array([cache.step(x) for x in self.X])
        np.testing.assert_allclose(outs, S.full_causal_attention(self.X, *self.W), atol=1e-12)

    def test_cache_growth(self):
        cache = S.KVCache(*self.W)
        self.assertEqual(cache.K.shape, (0, 4))
        for t, x in enumerate(self.X, 1):
            cache.step(x)
            self.assertEqual(cache.K.shape, (t, 4))
            self.assertEqual(cache.V.shape, (t, 4))

    def test_first_token_is_own_value(self):
        cache = S.KVCache(*self.W)
        np.testing.assert_allclose(cache.step(self.X[0]), self.X[0] @ self.W[2])

    def test_full_first_row(self):
        np.testing.assert_allclose(S.full_causal_attention(self.X, *self.W)[0], self.X[0] @ self.W[2])

    def test_full_causal_property(self):
        out1 = S.full_causal_attention(self.X, *self.W)
        X2 = self.X.copy(); X2[5:] = 0
        out2 = S.full_causal_attention(X2, *self.W)
        np.testing.assert_allclose(out1[:5], out2[:5])

    def test_cached_keys_are_projections(self):
        cache = S.KVCache(*self.W)
        for x in self.X[:3]:
            cache.step(x)
        np.testing.assert_allclose(cache.K, self.X[:3] @ self.W[1])
''',
"feedback": [
    ("test_matches_full", "Each step must attend over all cached keys including the new one, scaled by sqrt(d)."),
    ("test_cache_growth", "Start with zero-row arrays of shape (0, d) and append one row per step."),
    ("test_first_token_is_own_value", "With one cached token the softmax weight is 1, so output = its value."),
    ("test_full_causal_property", "Mask future keys with np.tril in the full version."),
],
},
]

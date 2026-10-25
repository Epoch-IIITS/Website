# Distributional Vectors with PPMI

## Learning outcomes

After this lesson you can:

- Count word–context co-occurrences in a window
- Compute positive pointwise mutual information
- Use PPMI rows as word vectors

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

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)

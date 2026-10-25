# Bigram Counts

## Learning outcomes

After this lesson you can:

- Pad sentences with <s> and </s>
- Count bigrams and unigram contexts
- Estimate maximum-likelihood bigram probabilities

## Intuition
To guess the next word, look at what usually follows the current one. After "of", "the" is
common; after "the", a noun. Counting adjacent word pairs (bigrams) captures this.

## Precise explanation
Pad each sentence with a start marker `<s>` and an end marker `</s>`:
`<s> i like tea </s>`. Bigrams are consecutive pairs: (`<s>`, i), (i, like), (like, tea),
(tea, `</s>`). The maximum-likelihood estimate is
$$P(w \mid w_\text{prev}) = \frac{C(w_\text{prev}, w)}{C(w_\text{prev}\ \text{as a context})},$$
where the denominator counts how often $w_\text{prev}$ appears as the **first** element of a
bigram. (`</s>` is never a context.) Unseen contexts have undefined probability — LM-02 adds
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

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)

# Multinomial Naive Bayes

## Learning outcomes

After this lesson you can:

- Estimate class priors and per-class word probabilities with Laplace smoothing
- Classify in log space
- Explain the conditional-independence assumption

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

## Library implementation

`sklearn.naive_bayes.MultinomialNB(alpha=1.0)` stores the same `class_log_prior_` and
`feature_log_prob_` and its `predict_log_proba` normalises the joint log-likelihood exactly as
yours does. It accepts sparse count matrices from `CountVectorizer`.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)

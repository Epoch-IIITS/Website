# A Text Classification Pipeline

## Learning outcomes

After this lesson you can:

- Build a TfidfVectorizer + LogisticRegression pipeline for raw text
- Use word bigrams and sublinear term frequency
- Read the most informative words from the model's coefficients

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
  grid search never leak test vocabulary (ML-07).
* `ngram_range=(1, 2)` adds word pairs, so "not good" becomes a feature of its own.
* `sublinear_tf=True` uses 1 + log(tf), so a word repeated ten times does not count ten times as much.
* For binary labels, `clf.coef_[0]` has one weight per feature; positive weights push towards
  class 1. `pipe.named_steps["tfidf"].get_feature_names_out()` gives the matching words.
* `C` is the inverse regularisation strength (ML-19).

## Worked example
Trained on product reviews, the largest positive weights go to "great", "love it", "highly
recommend"; the most negative to "terrible", "broke quickly", "waste of money".

## What the library does inside
The vectorizer is the TF-IDF of NL-10; logistic regression is the model you built
in ML-11, optimised with a quasi-Newton solver.

## Common mistakes
* Vectorising all texts before splitting.
* Reading weights from a model trained on unscaled counts (TF-IDF keeps them comparable).
* Assuming a word's weight is its effect in every context; correlated phrases share weight.

## Why this matters
This pipeline is often within a few points of far larger models, trains in seconds and explains
itself — a good first model for the review-sentiment project idea after this step.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)

# NL-P1 · Project idea: Review Sentiment Analyser

**Topic:** Natural Language Processing · ungraded

## Brief

Build a sentiment analyser for product or movie reviews that predicts positive or negative, explains
its decision with the words that mattered, and reports honestly where it fails (negation, sarcasm,
mixed reviews).

## You will use

- NL-03 Counting Words with Counter and CountVectorizer
- NL-10 Search with TfidfVectorizer and Cosine Similarity
- NL-15 A Text Classification Pipeline
- ML-16 Cross-Validation with scikit-learn

## Milestones

1. Load a labelled review dataset and look at the class balance and typical review length.
2. Train the TF-IDF + logistic regression pipeline and report cross-validated accuracy and F1.
3. List the top positive and negative phrases and check that they make sense.
4. Write an explain(review) function that shows each word's contribution to the score.
5. Collect 30 misclassified reviews and group them by cause (negation, sarcasm, wrong label, ...).

## Stretch goals

- Compare with the embedding-bag model in PyTorch.
- Add a third class for neutral or mixed reviews.
- Serve the model with FastAPI as in the 'Serve your model' project.

## Data

* IMDB movie reviews (50,000, balanced): on [Hugging Face](https://huggingface.co/datasets/stanfordnlp/imdb)
  or [Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews).
* Or write 100 short reviews of things you own and label them yourself.

## Run it yourself

```bash
pip install scikit-learn pandas datasets
python sentiment.py
```

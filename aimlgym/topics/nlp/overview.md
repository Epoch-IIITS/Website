# Natural Language Processing

**You will be able to:** Clean and tokenise text, count and vectorise it with CountVectorizer and TF-IDF, retrieve documents, compare strings, classify text with scikit-learn pipelines and error analysis, and learn word embeddings with PPMI and PyTorch.

**Topic prerequisites:** Deep Learning

Working with text: regular expressions, tokenisation and normalisation, word and character n-gram
counts with `Counter` and `CountVectorizer`, bag-of-words vectors, TF-IDF and cosine-similarity
search with scikit-learn, edit distance, Naive Bayes, a TF-IDF + logistic-regression text
classifier with error analysis, PPMI word vectors and analogies, and learned embeddings with
PyTorch's `nn.EmbeddingBag`.

**Packages:** standard library, `numpy`, `scikit-learn` and `torch`. The hand-written stopword,
character n-gram and retrieval steps, bigram counts and the suffix stemmer are **optional deep
dives**. **Project ideas:** a review sentiment analyser and semantic search for the club blog.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | NL-01 | [Regular Expressions for Text](regex-text/problem.md) | beginner | PY-16 |
| 2 | NL-02 | [Tokenize and Normalize](tokenize-normalize/problem.md) | beginner | NL-01 |
| 3 | NL-03 | [Counting Words with Counter and CountVectorizer](nlp-countvectorizer/problem.md) | beginner | NL-02, ML-02 |
| 4 | NL-04 | [Stopwords and Word Counts (optional deep dive)](stopword-counts/problem.md) | beginner | NL-02 |
| 5 | NL-05 | [Character n-grams with CountVectorizer](nlp-char-ngrams-sklearn/problem.md) | beginner | NL-03 |
| 6 | NL-06 | [Character n-grams by Hand (optional deep dive)](char-ngrams/problem.md) | beginner | NL-02 |
| 7 | NL-07 | [Bag-of-Words Vectors](bag-of-words/problem.md) | intermediate | NL-03 |
| 8 | NL-08 | [Bigram Counts with Sentence Markers (optional deep dive)](bigram-counts/problem.md) | intermediate | NL-04 |
| 9 | NL-09 | [TF-IDF](tf-idf/problem.md) | intermediate | NL-07 |
| 10 | NL-10 | [Search with TfidfVectorizer and Cosine Similarity](nlp-tfidf-retrieval/problem.md) | intermediate | NL-09 |
| 11 | NL-11 | [Cosine Similarity Retrieval (optional deep dive)](cosine-retrieval/problem.md) | intermediate | NL-09 |
| 12 | NL-12 | [Levenshtein Edit Distance](levenshtein/problem.md) | intermediate | NL-05 |
| 13 | NL-13 | [Rule-Based Suffix Stemmer (optional deep dive)](suffix-stemmer/problem.md) | advanced | NL-02 |
| 14 | NL-14 | [Multinomial Naive Bayes Text Classifier](naive-bayes-text/problem.md) | advanced | NL-07, ST-07 |
| 15 | NL-15 | [A Text Classification Pipeline](nlp-text-classifier/problem.md) | advanced | NL-14, NL-10 |
| 16 | NL-P1 | [Project idea: Review Sentiment Analyser](review-sentiment-analyser/project.md) | ungraded | NL-03, NL-10, NL-15, ML-16 |
| 17 | NL-16 | [Evaluating Text Classifiers](nlp-error-analysis/problem.md) | advanced | NL-15 |
| 18 | NL-17 | [PPMI Co-occurrence Matrix](ppmi-matrix/problem.md) | advanced | NL-07, NL-09 |
| 19 | NL-18 | [Word Embedding Analogies](embedding-analogy/problem.md) | advanced | NL-10, NL-17 |
| 20 | NL-19 | [Word Embeddings in PyTorch](nlp-embedding-bag/problem.md) | advanced | NL-18, DL-18 |
| 21 | NL-P2 | [Project idea: Semantic Search for the Club Blog](blog-semantic-search/project.md) | ungraded | NL-10, NL-05, NL-18, NL-19 |

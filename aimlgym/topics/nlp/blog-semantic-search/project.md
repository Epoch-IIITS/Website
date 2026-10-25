# NL-P2 · Project idea: Semantic Search for the Club Blog

**Topic:** Natural Language Processing · ungraded

## Brief

Build a search box for a collection of blog posts that finds posts by meaning, not only exact words:
"beginner python workshop" should also find "Intro to programming session". Compare keyword (TF-IDF)
search with embedding-based search on the same queries.

## You will use

- NL-10 Search with TfidfVectorizer and Cosine Similarity
- NL-05 Character n-grams with CountVectorizer
- NL-18 Word Embedding Analogies
- NL-19 Word Embeddings in PyTorch

## Milestones

1. Collect 50–200 posts (titles and text) into a JSON file.
2. Build TF-IDF search and a small command-line interface that prints the top five results.
3. Write 20 test queries with the posts you expect, and measure how often the right post is in the top three.
4. Add character n-gram search for typos and compare the scores.
5. Add embedding search with a sentence-embedding model and combine it with TF-IDF (for example by averaging ranks).

## Stretch goals

- Add filters (author, date, tag) alongside the text search.
- Highlight the matching sentences in each result.
- Expose the search as a FastAPI endpoint for the website.

## Data

Use the Epoch blog posts you can access, or any set of articles you write or collect. Sentence-embedding
models such as those in the `sentence-transformers` library download weights the first time they run.

## Run it yourself

```bash
pip install scikit-learn numpy sentence-transformers
python search.py "beginner python workshop"
```

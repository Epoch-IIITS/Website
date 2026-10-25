# Word Embeddings in PyTorch

## Learning outcomes

After this lesson you can:

- Map tokens to integer ids with a vocabulary that has an unknown token
- Average learned word embeddings with nn.EmbeddingBag and offsets
- Train an embedding-bag classifier end to end

## Intuition
PPMI vectors (NL-17) are computed from counts. A neural model can instead **learn** a
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

## References

- [torch.nn.EmbeddingBag](https://docs.pytorch.org/docs/stable/generated/torch.nn.EmbeddingBag.html) — PyTorch (`S127`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)

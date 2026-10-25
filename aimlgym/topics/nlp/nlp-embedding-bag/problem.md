# NL-19 · Word Embeddings in PyTorch

**Topic:** Natural Language Processing · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** NL-18 Word Embedding Analogies, DL-18 A Full Training Loop

Read the lesson first: [article.md](article.md)

## Task

1. `build_vocab(texts, min_count=1)` splits lowercased texts on whitespace and returns a dict with
   `"<unk>": 0` and words with count ≥ `min_count` numbered from 1 by count descending, then
   alphabetically.
2. `encode(texts, vocab)` returns `(ids, offsets)` as `torch.long` tensors, mapping unknown words to 0.
3. `class BagClassifier(nn.Module)` with `__init__(self, vocab_size, dim, n_classes)` storing
   `self.embedding = nn.EmbeddingBag(vocab_size, dim, mode="mean")` and `self.fc = nn.Linear(dim, n_classes)`;
   `forward(ids, offsets)`.
4. `train_bag(texts, labels, dim=16, epochs=30, lr=0.05, seed=0)` builds the vocabulary, calls
   `torch.manual_seed(seed)`, creates the model and trains on the **whole set each epoch** (one batch)
   with Adam and `CrossEntropyLoss`. Return `(model, vocab, history)` with the model in `eval()` mode.

## Hints

<details><summary>Hint 1</summary>

Vocabulary: `Counter` over all words, keep those with enough counts, sort by `(-count, word)`, and number from 1.

</details>

<details><summary>Hint 2</summary>

Encode: extend one list of ids per text, recording `len(ids)` before each text as its offset.

</details>

<details><summary>Hint 3</summary>

Training: one forward pass on all texts per epoch — `loss = loss_fn(model(ids, offsets), y)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_vocab_order` | Reserve 0 for <unk>, then number words by (-count, word). |
| `test_encode_offsets_and_unknown` | Offsets are start positions; unknown words map to 0. |
| `test_model_output_and_mean` | Use nn.EmbeddingBag(vocab_size, dim, mode='mean') followed by nn.Linear. |
| `test_reproducible_and_eval` | Seed before creating the model and finish in eval() mode. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The vocabulary reserves id 0 for unknown words so any text can be encoded. Concatenating ids and
recording where each text starts lets `EmbeddingBag` average variable-length texts without padding.
The classifier learns the embeddings and the output layer together.

## References

- [torch.nn.EmbeddingBag](https://docs.pytorch.org/docs/stable/generated/torch.nn.EmbeddingBag.html) — PyTorch (`S127`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)

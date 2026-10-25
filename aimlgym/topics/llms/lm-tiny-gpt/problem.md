# LM-16 · A Tiny GPT in PyTorch

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** LM-15 Incremental Decoding with a KV Cache, LM-11 A Transformer Block as nn.Module

Read the lesson first: [article.md](article.md)

## Task

1. `class TinyGPT(nn.Module)` with `__init__(self, vocab_size, context, d_model=32, n_heads=2, n_layers=1)`
   storing `self.context`, `self.tok_emb = nn.Embedding(vocab_size, d_model)`,
   `self.pos_emb = nn.Embedding(context, d_model)`, `self.blocks = nn.TransformerEncoder(nn.TransformerEncoderLayer(d_model, n_heads, 4 * d_model, dropout=0.0, activation="gelu", batch_first=True, norm_first=True), n_layers, enable_nested_tensor=False)`,
   `self.ln_f = nn.LayerNorm(d_model)` and `self.head = nn.Linear(d_model, vocab_size)`.
   `forward(idx)` returns logits `(B, T, vocab)` using the causal mask
   `nn.Transformer.generate_square_subsequent_mask(T)` with `is_causal=True`.
2. `train_tiny_gpt(text, context=16, steps=200, batch_size=32, lr=3e-3, seed=0)`: vocabulary
   `chars = sorted(set(text))`; `torch.manual_seed(seed)`; model; AdamW; each step draws `batch_size`
   start positions with `torch.randint(len(data) - context - 1, (batch_size,), generator=g)`
   (`g = torch.Generator().manual_seed(seed)`). Return `(model, stoi, itos, losses)` with the model in
   `eval()` mode, `stoi` a dict and `itos` a list.
3. `generate(model, stoi, itos, prompt, n_new)` returns the prompt plus `n_new` greedily generated
   characters, feeding at most the last `model.context` characters. Raise `ValueError` for prompt
   characters outside the vocabulary.

## Hints

<details><summary>Hint 1</summary>

In forward: `T = idx.shape[1]`, add `self.pos_emb(torch.arange(T))` to the token embeddings, run the encoder with the mask, then `self.head(self.ln_f(x))`.

</details>

<details><summary>Hint 2</summary>

Build a batch with `torch.stack([data[i:i + context] for i in ix])` and the targets shifted by one.

</details>

<details><summary>Hint 3</summary>

Generation loop: crop `ids[-model.context:]`, take `logits[0, -1].argmax()`, append; use `torch.no_grad()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_loss_falls` | Targets are the inputs shifted by one; use cross-entropy over all positions. |
| `test_generates_pattern` | Greedy generation takes argmax of the last position's logits. |
| `test_output_shape_and_causality` | Pass the causal mask and is_causal=True to the encoder. |
| `test_long_prompt_is_cropped` | Feed only the last model.context ids when generating. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Embeddings turn characters and positions into vectors, the causal encoder layers mix information from
earlier positions only, and the head scores every possible next character. Training samples random
windows and their one-step-shifted targets; greedy generation repeatedly appends the most likely
next character within the context window.

## References

- [nanoGPT](https://github.com/karpathy/nanoGPT) — Andrej Karpathy (`S128`)
- [torch.nn.TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html) — PyTorch (`S129`)

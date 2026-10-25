# A Tiny GPT in PyTorch

## Learning outcomes

After this lesson you can:

- Assemble token and position embeddings, transformer blocks and an output head into a GPT
- Train it on character windows with next-token cross-entropy
- Generate text greedily with a context window

## Intuition
A GPT reads a window of tokens and predicts, at every position, the next token. Train it on
windows of text with cross-entropy and it learns the patterns of that text; generate by repeatedly
predicting a token and appending it. A character-level model with one block, trained for a few
hundred steps on a CPU, already reproduces simple text.

## Precise explanation
```python
x = self.tok_emb(idx) + self.pos_emb(torch.arange(T))        # (B, T, d)
x = self.blocks(x, mask=causal_mask, is_causal=True)          # nn.TransformerEncoder, pre-norm layers
logits = self.head(self.ln_f(x))                              # (B, T, vocab)
loss = F.cross_entropy(logits.view(-1, V), targets.view(-1))  # targets = inputs shifted by one
```

* Training pairs come from random windows: `x = data[i:i+T]`, `y = data[i+1:i+T+1]`. Every position
  is a training example, so one window of 16 characters gives 16 predictions.
* Positions are learned with `nn.Embedding(context, d)`; the model cannot read more than `context`
  tokens, so generation crops the input to the last `context` tokens.
* The causal mask (LM-11) prevents position t from seeing tokens after t.
* Greedy generation takes the argmax of the last position's logits; LM-13 sampling gives
  more varied text.
* An untrained model has loss ≈ ln(V); a model that has learned repetitive text approaches 0.

## Worked example
Trained for 200 steps on "hello world. " repeated, the loss drops from about ln(9) ≈ 2.2 to below 0.2,
and greedy generation from "hello w" continues "orld. hello world".

## Common mistakes
* Targets not shifted by one, so the model learns to copy its input.
* Generating with prompts longer than the context without cropping.
* Forgetting `model.eval()` and `torch.no_grad()` while generating.

## Why this matters
This is the architecture of GPT-2 and its successors in miniature; scaling up the data, context and
number of blocks is most of the remaining difference. The poem-generator project idea trains it on
your own text.

## References

- [nanoGPT](https://github.com/karpathy/nanoGPT) — Andrej Karpathy (`S128`)
- [torch.nn.TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html) — PyTorch (`S129`)

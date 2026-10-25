# A Full Training Loop

## Learning outcomes

After this lesson you can:

- Train a classifier with a DataLoader, CrossEntropyLoss and an optimiser
- Switch between train() and eval() and evaluate under torch.no_grad()
- Record the loss per epoch and make training reproducible with a seed

## Intuition
Everything comes together: a model, a loss, an optimiser and batches of data. One **epoch** passes
over the whole training set once; after each batch the model's weights move a little. Watching the
average loss per epoch tells you whether learning is working.

## Precise explanation
```python
torch.manual_seed(seed)                                   # initial weights
model = MLP(n_in, n_hidden, n_classes)
loss_fn = nn.CrossEntropyLoss()                           # softmax + negative log-likelihood
opt = torch.optim.Adam(model.parameters(), lr=lr)
for epoch in range(epochs):
    model.train()
    total = 0.0
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)                     # logits (B, C), labels (B,) int64
        loss.backward()
        opt.step()
        total += loss.item() * len(yb)
    history.append(total / len(dataset))                  # mean loss over the epoch

model.eval()
with torch.no_grad():
    predictions = model(X).argmax(dim=1)
```

* `nn.CrossEntropyLoss` takes raw logits and integer class labels; it is the softmax +
  DL-03 you wrote earlier, computed stably.
* `model.train()` / `model.eval()` switch layers such as dropout and batch normalisation
  (next steps) between their training and inference behaviour.
* `torch.no_grad()` skips graph building during evaluation: faster, and no accidental gradients.
* Weight the batch loss by batch size when averaging, so a short last batch counts correctly.

## Worked example
XOR (four points, two classes) cannot be separated by a line. An MLP with 16 hidden units trained
with Adam (lr 0.05) for 100 epochs drives the loss from about 0.7 to below 0.05 and classifies all
four points correctly.

## What the library does inside
The loop is the one you write by hand with NumPy in DL-19, the optional deep dive
after this step — forward pass, loss, backward pass, update — with autograd computing the gradients.

## Common mistakes
* Passing softmax probabilities to `CrossEntropyLoss` (it expects logits).
* Forgetting `model.eval()` before evaluating a model with dropout or batch normalisation.
* Averaging batch losses without weighting by batch size.
* Seeding after the model is created, so the initial weights are not reproducible.

## Why this matters
This loop, with a different model and dataset, trains image classifiers, language models and
policies. The digit-recogniser project idea after this step is the same loop on real images.

## References

- [Optimizing Model Parameters (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) — PyTorch (`S106`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)

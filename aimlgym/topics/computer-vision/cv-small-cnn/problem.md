# CV-21 · A Small CNN in PyTorch

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy, torch

**Builds on:** CV-20 Contours and Bounding Boxes, DL-18 A Full Training Loop

Read the lesson first: [article.md](article.md)

## Task

1. `class SmallCNN(nn.Module)` with `__init__(self, n_classes=3, size=16)`: `self.features` and
   `self.classifier` exactly as in the lesson, with the classifier input `16 * (size // 4) ** 2`.
   `forward(x)` returns logits.
2. `train_cnn(images, labels, epochs=8, lr=0.01, seed=0)` where `images` is an array
   `(n, size, size)` of uint8 pixels: scale to [0, 1], add the channel dimension, call
   `torch.manual_seed(seed)`, build `SmallCNN(max(labels) + 1, size)`, and train with Adam,
   `CrossEntropyLoss` and a `DataLoader(batch_size=32, shuffle=True, generator=torch.Generator().manual_seed(seed))`.
   Return `(model, history)` with the mean loss per epoch and the model in `eval()` mode.
3. `predict(model, images)` returns a list of class indices for uint8 images, scaled the same way.

## Hints

<details><summary>Hint 1</summary>

Write a helper `to_tensor(images)` returning `torch.as_tensor(np.asarray(images), dtype=torch.float32)[:, None] / 255`.

</details>

<details><summary>Hint 2</summary>

The classifier is `nn.Linear(16 * (size // 4) ** 2, n_classes)`; forward flattens with `torch.flatten(x, 1)`.

</details>

<details><summary>Hint 3</summary>

The training loop is the one from the training-loop step, with the epoch loss weighted by batch size.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_shapes_through_network` | Two padded 3×3 convolutions with 2×2 max pooling; classifier input 16 * (size // 4) ** 2. |
| `test_learns_shapes` | Scale pixels to [0, 1], add the channel axis and train with Adam and CrossEntropyLoss. |
| `test_reproducible` | Seed before building the model and pass a seeded generator to the DataLoader. |
| `test_eval_mode_and_types` | Call model.eval() and return predictions as a list of ints. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Two convolution blocks turn a 16×16 image into 16 feature maps of 4×4; one linear layer maps them to
class scores. Training is the standard loop; scaling pixels to [0, 1] and adding the channel axis
happen in one helper used by both training and prediction.

## References

- [Training a Classifier (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html) — PyTorch (`S124`)
- [torch.nn.Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) — PyTorch (`S093`)

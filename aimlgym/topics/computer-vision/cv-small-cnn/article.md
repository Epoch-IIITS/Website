# A Small CNN in PyTorch

## Learning outcomes

After this lesson you can:

- Stack Conv2d, ReLU and MaxPool2d layers into a CNN
- Compute the flattened feature size before the classifier layer
- Train the CNN on generated images and evaluate it on new ones

## Intuition
A convolutional network learns its own filters. Early layers find edges and blobs, later layers
combine them into parts; pooling shrinks the maps so later filters see larger regions. Because the
same filter slides everywhere, the network recognises a pattern wherever it appears.

## Precise explanation
For 1-channel 16×16 images and 3 classes:

```python
self.features = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),    # 8 × 8 × 8
    nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 16 × 4 × 4
)
self.classifier = nn.Linear(16 * 4 * 4, n_classes)

def forward(self, x):                     # x: (B, 1, 16, 16), float32 in [0, 1]
    return self.classifier(torch.flatten(self.features(x), 1))
```

* `padding=1` with a 3×3 kernel keeps height and width; each `MaxPool2d(2)` halves them.
* The classifier's input size is channels × height × width after the last pool — compute it
  (CV-13) or run a dummy tensor through `features` and read the shape.
* `nn.Conv2d(in, out, k)` has out·in·k·k + out parameters — far fewer than a dense layer on raw
  pixels, which is why CNNs generalise well on images.
* Images become tensors of shape (B, C, H, W) with values scaled to [0, 1]; labels are `long`.

## Worked example
On synthetic 16×16 images of horizontal bars, vertical bars and square outlines at random
positions, this network reaches over 95% accuracy on new images after a few epochs, while a
logistic regression on raw pixels struggles because the shapes move around.

## What the library does inside
Each `Conv2d` computes the multi-channel sums of CV-15 for all positions at once; the
training loop is the one from DL-18.

## Common mistakes
* A wrong flattened size, giving "mat1 and mat2 shapes cannot be multiplied".
* Feeding (B, H, W) without the channel dimension, or channels-last (B, H, W, C) arrays.
* Forgetting to scale uint8 pixels to [0, 1].

## Why this matters
This is a miniature of the networks behind image classification, medical imaging and visual
inspection; the shape-sorter project idea builds on it.

## References

- [Training a Classifier (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html) — PyTorch (`S124`)
- [torch.nn.Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) — PyTorch (`S093`)

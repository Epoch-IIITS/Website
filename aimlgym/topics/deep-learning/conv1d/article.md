# 1-D Convolution

## Learning outcomes

After this lesson you can:

- Implement deep-learning style convolution (cross-correlation)
- Apply padding and stride
- Compute the output length formula

## Intuition
Slide a small window (the **kernel**) along a signal; at each position, take the dot product of
the kernel with the part of the signal under it. A kernel [−1, 1] detects increases; [1/3]×3
smooths.

## Precise explanation
Deep-learning libraries implement **cross-correlation** (no kernel flip) and still call it
convolution:
$$y_i = b + \sum_{j=0}^{k-1} x_{is + j}\, w_j,$$
after zero-padding $p$ values on both ends. Output length (CS231n formula):
$$n_\text{out} = \left\lfloor \frac{n + 2p - k}{s} \right\rfloor + 1.$$
NumPy's `np.convolve` flips the kernel (mathematical convolution); `np.correlate(x, w, "valid")`
matches the DL definition for stride 1, no padding.

## Worked example
x = [1, 2, 3, 4, 5], w = [1, 0, −1], stride 1: [1−3, 2−4, 3−5] = [−2, −2, −2]; length
(5 − 3)/1 + 1 = 3. With stride 2: positions 0 and 2 → [−2, −2]. With padding 1: x becomes
[0,1,2,3,4,5,0] → length 5: [−2, −2, −2, −2, 4].

## Common mistakes
* Flipping the kernel (using `np.convolve`).
* Off-by-one in the number of windows.
* Padding only one side.

## Why this matters
Convolutions power audio models and text CNNs, and their 2-D version is the core of computer
vision (CV-10).

## Library implementation

With stride 1, `np.correlate(np.pad(x, p), kernel, mode="valid")` computes the same values
(NumPy's `np.convolve` flips the kernel; deep-learning "convolution" does not).
`torch.nn.functional.conv1d` adds batches, channels and strides.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

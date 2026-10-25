# Batch Normalisation with nn.BatchNorm1d

## Learning outcomes

After this lesson you can:

- Explain how BatchNorm1d uses batch statistics in training and running statistics in evaluation
- Compute the running mean and variance updates with momentum
- Recognise the biased and unbiased variances BatchNorm uses

## Intuition
Batch normalisation standardises each feature using the mean and variance of the current batch,
then lets the network rescale and shift it with learned parameters γ and β. That keeps activations
in a well-behaved range and speeds up training. At prediction time there may be a single example,
so the layer uses **running** averages of the statistics it saw during training.

## Precise explanation
For each feature, in training mode:

$$\hat x = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}},\quad y = \gamma \hat x + \beta,$$

with the batch mean μ_B and the **biased** batch variance σ²_B (divide by n). The running
statistics are updated after each batch:

running_mean ← (1 − m)·running_mean + m·μ_B,  running_var ← (1 − m)·running_var + m·s²_B,

where m is `momentum` (default 0.1) and s²_B is the **unbiased** variance (divide by n − 1).
They start at 0 and 1. In `eval()` mode the layer uses running_mean and running_var instead of
batch statistics. γ starts at 1, β at 0, ε = 1e−5.

## Worked example
One batch with feature values [1, 3]: μ_B = 2, biased variance 1 → outputs ≈ [−1, 1]; unbiased
variance 2, so with m = 0.1 running_mean = 0.2 and running_var = 0.9·1 + 0.1·2 = 1.1.

## What the library does inside
The training-mode computation is your DL-23 (the optional deep dive after this
step); the layer adds the running averages and the mode switch.

## Common mistakes
* Evaluating in training mode, so predictions depend on the other examples in the batch.
* Training with batch size 1 (the variance is undefined; PyTorch raises an error).
* Expecting the running variance to use the same (biased) estimate as the normalisation.

## Why this matters
Batch normalisation is standard in convolutional networks; its train/eval behaviour is a common
source of "it worked in training but not in production" bugs.

## References

- [torch.nn.BatchNorm1d](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html) — PyTorch (`S112`)
- [Build the Neural Network (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) — PyTorch (`S104`)

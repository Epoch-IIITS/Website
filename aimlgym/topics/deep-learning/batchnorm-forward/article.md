# Batch Normalization

## Learning outcomes

After this lesson you can:

- Normalise activations with batch statistics
- Maintain running averages for evaluation
- Apply learnable scale and shift

## Intuition
Layer inputs drift as earlier layers learn. Batch normalisation standardises each feature using
the current mini-batch's mean and variance, then lets the network re-scale and re-shift with
learned parameters — making training faster and less sensitive to initialisation.

## Precise explanation
For a batch $x$ `(n, d)`, per feature:
$$\mu_B = \text{mean}(x),\ \sigma_B^2 = \text{var}(x)\ (\text{population}),\quad
\hat x = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}},\quad y = \gamma \hat x + \beta.$$
Running statistics for evaluation (PyTorch-style momentum, D2L describes the same idea):
$$\mu_\text{run} \leftarrow (1-m)\mu_\text{run} + m\,\mu_B,\qquad
\sigma^2_\text{run} \leftarrow (1-m)\sigma^2_\text{run} + m\,\sigma^2_{B,\text{unbiased}},$$
where the running variance uses the unbiased $n/(n-1)$ batch variance (as PyTorch does).
Evaluation uses the running statistics, so a single example gives a deterministic output.
Initial values: $\gamma = 1$, $\beta = 0$, $\mu_\text{run} = 0$, $\sigma^2_\text{run} = 1$.

## Worked example
x = [[1], [3]]: μ = 2, σ² = 1 → x̂ ≈ [−1, 1] (ε small). Running mean after one step with
m = 0.1: 0.2; running var: 0.9·1 + 0.1·2 = 1.1 (unbiased var = 2).

## Common mistakes
* Using batch statistics at evaluation time.
* Normalising across features instead of across the batch (that is layer norm).
* Updating running statistics during evaluation.

## Why this matters
Batch norm is common in CNNs; its train/eval distinction appears again in dropout and in
federated settings where client batch statistics differ.

## Library implementation

`torch.nn.BatchNorm1d(n_features, momentum=0.1, eps=1e-5)` uses the same conventions: batch
statistics with the biased variance in training mode, running averages updated with the
**unbiased** variance, and running statistics in evaluation mode (`model.eval()`).

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)

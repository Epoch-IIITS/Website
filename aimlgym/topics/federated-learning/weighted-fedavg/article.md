# Weighted Federated Averaging

## Learning outcomes

After this lesson you can:

- Aggregate client models weighted by dataset size
- Handle parameter dictionaries
- Validate shapes and weights

## Intuition
The server never sees data — only model parameters trained by clients. It combines them by averaging,
giving clients with more data proportionally more say.

## Precise explanation (McMahan et al., 2016)
With client parameters $w_k$ and sample counts $n_k$, $N = \sum_k n_k$:
$$w = \sum_k \frac{n_k}{N} w_k.$$
For models with several tensors, average each tensor (dict key) separately with the same weights.
A client with $n_k = 0$ contributes nothing; if all $n_k = 0$ the average is undefined.
The unweighted mean is biased towards small clients' data distributions.

## Worked example
Client A: w = [1, 2], n = 10; client B: w = [3, 6], n = 30 → 0.25·[1, 2] + 0.75·[3, 6] = [2.5, 5.0].

## Common mistakes
* Plain mean instead of weighted mean.
* Aggregating parameters with mismatched shapes (different model versions).
* Integer division in weights.

## Why this matters
FedAvg's aggregation step is the heart of federated learning; secure aggregation (FL-12) and DP
(FL-13) modify exactly this step.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)

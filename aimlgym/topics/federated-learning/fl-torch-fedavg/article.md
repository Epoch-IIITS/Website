# FedAvg with PyTorch state_dicts

## Learning outcomes

After this lesson you can:

- Average client state_dicts weighted by their sample counts
- Handle integer buffers that must not be averaged
- Run several federated rounds and watch the global model improve

## Intuition
After a round of local training, each client has slightly different weights. FedAvg combines them
into the next global model by averaging each parameter, giving clients with more data more say —
exactly the weighted average of FL-02, now applied tensor by tensor to a state dict.

## Precise explanation
$$\theta^{\text{global}}_k = \sum_i \frac{n_i}{\sum_j n_j}\,\theta^{(i)}_k \quad\text{for every tensor } k.$$

```python
total = sum(counts)
averaged = {k: sum(state[k] * (n / total) for state, n in zip(states, counts)) for k in states[0]}
model.load_state_dict(averaged)
```

* All clients must share one architecture, so their state dicts have the same keys and shapes.
* Floating-point tensors are averaged. **Integer buffers** — for example BatchNorm's
  `num_batches_tracked` — cannot be averaged meaningfully; copy them from the first client.
* A **round**: send the global model to every client (FL-05), collect
  `(state_dict, n)`, average, load into the global model. Repeat for several rounds.
* With non-IID clients (FL-04) local models drift apart; more rounds with fewer local
  epochs, or FedProx (FL-14), help.

## Worked example
Two clients with 30 and 10 examples and weights w = 1.0 and 2.0 give 0.75·1.0 + 0.25·2.0 = 1.25.

## Common mistakes
* Averaging without weights when client sizes differ.
* Averaging `num_batches_tracked` and getting a float or a type error.
* Reusing the same seed for every client, so all shuffles are identical.

## Why this matters
This is the algorithm behind federated keyboards and hospital collaborations; frameworks such as Flower
implement the same loop across real devices. The project idea after this step simulates departments.

## References

- [Saving and Loading Models (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) — PyTorch (`S108`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)

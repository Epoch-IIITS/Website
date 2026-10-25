# FL-11 · FedAvg with PyTorch state_dicts

**Topic:** Federated Learning · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** FL-10 Full FedAvg Training Loop, FL-05 Client Training with a PyTorch Model

Read the lesson first: [article.md](article.md)

## Task

1. `average_states(states, counts)` returns a new state dict: floating-point tensors are the weighted
   average by `counts`; other tensors (integers) are copied from the first state. Raise `ValueError`
   if the lists are empty, differ in length, any count is ≤ 0, or the key sets differ.
2. `federated_training(model, clients, rounds, epochs=1, lr=0.1, seed=0)` where `clients` is a list of
   `(X, y)`: for each round, call `client_update(model, X, y, epochs, lr, seed=seed + 1000 * round_index + client_index)`
   for every client, average the results and load them into `model`. Return the list of global MSE
   losses on all clients' data combined, measured **after** each round.

Copy your `client_update` from the previous step into this file.

## Hints

<details><summary>Hint 1</summary>

Check `tensor.is_floating_point()` to decide between averaging and copying.

</details>

<details><summary>Hint 2</summary>

`sum(state[k] * (n / total) for state, n in zip(states, counts))` averages one tensor.

</details>

<details><summary>Hint 3</summary>

After each round, measure `nn.functional.mse_loss(model(X_all), y_all)` under `torch.no_grad()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_weighted_average` | Weight each client by n_i / total and copy integer tensors from the first state. |
| `test_batchnorm_model` | num_batches_tracked is an integer buffer: copy it instead of averaging. |
| `test_training_improves` | Each round: update every client from the current model, average, load_state_dict. |
| `test_invalid` | Reject empty input, non-positive counts and mismatched keys. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The average is taken tensor by tensor with weights proportional to client data; integer buffers are
copied because they cannot be averaged. Each round sends the current global model to every client,
averages the returned weights and loads them, and the combined-data loss shows the global model improving.

## References

- [Saving and Loading Models (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) — PyTorch (`S108`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)

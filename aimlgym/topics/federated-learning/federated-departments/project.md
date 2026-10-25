# FL-P1 · Project idea: Federated Training across Departments

**Topic:** Federated Learning · ungraded

## Brief

Simulate several college departments that want a shared model (for example, predicting which students
need extra support) without pooling their records. Compare federated training with central training,
and see how uneven, non-IID data across departments affects the result.

## You will use

- FL-04 Label-Skewed (non-IID) Partition
- FL-05 Client Training with a PyTorch Model
- FL-11 FedAvg with PyTorch state_dicts
- FL-13 Differentially Private Aggregation
- FL-14 FedProx Local Objective

## Milestones

1. Generate or load a tabular dataset and split it into 4–6 'departments' with different label mixes.
2. Train a central model on all data as the reference.
3. Run FedAvg with the PyTorch steps and plot global accuracy per round.
4. Vary local epochs and client sampling and record how many rounds each setting needs.
5. Add update clipping and noise (differential privacy) and measure the accuracy cost.

## Stretch goals

- Implement FedProx in PyTorch and compare on the most uneven split.
- Run the same experiment with the Flower framework, with clients as separate processes.
- Personalise: fine-tune the global model on each department and report per-department accuracy.

## Data

Synthetic data from `sklearn.datasets.make_classification` works well; split it by a feature to create
non-IID departments. See the [Flower framework documentation](https://flower.ai/docs/framework/) for
running real federated clients.

## Run it yourself

```bash
pip install torch scikit-learn flwr
python simulate.py --clients 5 --rounds 30
```

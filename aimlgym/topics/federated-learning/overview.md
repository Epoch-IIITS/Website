# Federated Learning

**You will be able to:** Simulate clients and partitions, train client copies of PyTorch models, aggregate state_dicts with weighted FedAvg, and add client sampling, clipping, secure aggregation, differential privacy and FedProx.

**Topic prerequisites:** Deep Learning

Training a model across many clients without collecting their data. The topic simulates clients
in one process: IID and label-skewed partitions, weighted averaging, client updates as deltas,
client training of a PyTorch model copy, a FedAvg round and full training loop, FedAvg over
PyTorch `state_dict`s, client sampling, update clipping, secure aggregation with pairwise masks,
differentially private aggregation and FedProx.

**Packages:** `numpy` and `torch`. The privacy steps teach the mechanics (clipping, noise,
masking); they do not compute formal privacy guarantees. Local SGD in NumPy is an **optional deep
dive**. **Project idea:** federated training across departments, with a pointer to the Flower
framework.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | FL-01 | [IID Client Partitioning](iid-partition/problem.md) | beginner | ML-16 |
| 2 | FL-02 | [Weighted Federated Averaging](weighted-fedavg/problem.md) | beginner | FL-01 |
| 3 | FL-03 | [Client Updates as Deltas](client-delta/problem.md) | beginner | FL-02 |
| 4 | FL-04 | [Label-Skewed (non-IID) Partition](label-skew-partition/problem.md) | beginner | FL-01 |
| 5 | FL-05 | [Client Training with a PyTorch Model](fl-torch-local-training/problem.md) | intermediate | FL-04, DL-18 |
| 6 | FL-06 | [Local SGD on a Client (optional deep dive)](local-sgd/problem.md) | intermediate | ML-10, FL-03 |
| 7 | FL-07 | [One FedAvg Round](fedavg-round/problem.md) | intermediate | FL-02, FL-05 |
| 8 | FL-08 | [Seeded Client Sampling](client-sampling/problem.md) | intermediate | FL-07 |
| 9 | FL-09 | [Clipping Client Updates](update-clipping/problem.md) | intermediate | FL-03 |
| 10 | FL-10 | [Full FedAvg Training Loop](fedavg-training/problem.md) | advanced | FL-07, FL-08 |
| 11 | FL-11 | [FedAvg with PyTorch state_dicts](fl-torch-fedavg/problem.md) | advanced | FL-10, FL-05 |
| 12 | FL-12 | [Secure Aggregation with Pairwise Masks](secure-aggregation/problem.md) | advanced | FL-02 |
| 13 | FL-13 | [Differentially Private Aggregation](dp-aggregation/problem.md) | advanced | FL-09, FL-02 |
| 14 | FL-14 | [FedProx Local Objective](fedprox/problem.md) | advanced | FL-05, FL-10 |
| 15 | FL-P1 | [Project idea: Federated Training across Departments](federated-departments/project.md) | ungraded | FL-04, FL-05, FL-11, FL-13, FL-14 |

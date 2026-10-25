# Deep Learning

**You will be able to:** Understand neurons, activations, losses, backpropagation and optimisers in NumPy, then build, train, debug, save and reproduce PyTorch models with nn.Module, autograd, torch.optim, DataLoader, dropout, batch normalisation and Conv1d.

**Topic prerequisites:** Machine Learning

Neural networks in two passes. In NumPy you write activations, softmax, cross-entropy, dense
layers, a tiny scalar autograd engine and backpropagation, and SGD with momentum. In PyTorch you
then use tensors, `nn.Module`, autograd, custom gradients with `gradcheck`, `torch.optim`,
`Dataset` and `DataLoader`, a full training loop, dropout, batch normalisation and `Conv1d`, and
finish with saving, loading, reproducibility and debugging training.

**Packages:** `numpy`, then `torch` (CPU). Everything trains in about a second. The NumPy versions
of the MLP, gradient check, Adam, XOR training, dropout, batch normalisation and convolution stay
as **optional deep dives** after their PyTorch steps. **Project ideas:** a handwritten digit
recogniser and a training-diagnostics notebook.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | DL-01 | [Activation Functions](activations/problem.md) | beginner | ML-11 |
| 2 | DL-02 | [Numerically Stable Softmax](stable-softmax/problem.md) | beginner | DL-01, MA-02 |
| 3 | DL-03 | [Cross-Entropy Loss](cross-entropy/problem.md) | beginner | DL-02 |
| 4 | DL-04 | [Dense Layer Forward Pass](dense-forward/problem.md) | beginner | DL-01, NP-06 |
| 5 | DL-05 | [PyTorch Tensors](torch-tensors/problem.md) | beginner | DL-04 |
| 6 | DL-06 | [Models with nn.Module](torch-mlp-module/problem.md) | beginner | DL-05 |
| 7 | DL-07 | [MLP Forward Pass (optional deep dive)](mlp-forward/problem.md) | beginner | DL-04 |
| 8 | DL-08 | [A Tiny Autograd Engine](scalar-autograd/problem.md) | intermediate | DL-06, MA-11 |
| 9 | DL-09 | [Autograd in PyTorch](torch-autograd/problem.md) | intermediate | DL-08, DL-06 |
| 10 | DL-10 | [Backprop Through One Neuron](neuron-backprop/problem.md) | intermediate | DL-08 |
| 11 | DL-11 | [Backpropagation Through a Dense Layer](dense-backward/problem.md) | intermediate | DL-10 |
| 12 | DL-12 | [Custom Gradients and gradcheck](torch-gradcheck/problem.md) | intermediate | DL-11, DL-09 |
| 13 | DL-13 | [Gradient Checking by Hand (optional deep dive)](gradient-check/problem.md) | intermediate | DL-11, MA-14 |
| 14 | DL-14 | [SGD with Momentum](sgd-momentum/problem.md) | intermediate | DL-11, MA-13 |
| 15 | DL-15 | [Optimisers in torch.optim](torch-optimizers/problem.md) | advanced | DL-14, DL-12 |
| 16 | DL-16 | [The Adam Optimiser (optional deep dive)](adam-optimizer/problem.md) | advanced | DL-14 |
| 17 | DL-17 | [Datasets and DataLoader](torch-datasets/problem.md) | advanced | DL-15 |
| 18 | DL-18 | [A Full Training Loop](torch-training-loop/problem.md) | advanced | DL-17 |
| 19 | DL-19 | [Train an MLP on XOR (optional deep dive)](train-xor-mlp/problem.md) | advanced | DL-11, DL-14 |
| 20 | DL-P1 | [Project idea: Handwritten Digit Recogniser](digit-recogniser/project.md) | ungraded | DL-06, DL-17, DL-18 |
| 21 | DL-20 | [Dropout with train() and eval()](torch-dropout/problem.md) | advanced | DL-18 |
| 22 | DL-21 | [Inverted Dropout (optional deep dive)](inverted-dropout/problem.md) | advanced | DL-19, NP-10 |
| 23 | DL-22 | [Batch Normalisation with nn.BatchNorm1d](torch-batchnorm/problem.md) | advanced | DL-20 |
| 24 | DL-23 | [Batch Normalization by Hand (train/eval) (optional deep dive)](batchnorm-forward/problem.md) | advanced | DL-21 |
| 25 | DL-24 | [1-D Convolution with nn.Conv1d](torch-conv1d/problem.md) | advanced | DL-22, NP-14 |
| 26 | DL-25 | [1D Convolution by Hand (valid, stride) (optional deep dive)](conv1d/problem.md) | advanced | DL-04, NP-14 |
| 27 | DL-26 | [Saving, Loading and Reproducibility](torch-save-load/problem.md) | advanced | DL-24 |
| 28 | DL-27 | [Debugging Training](torch-debugging/problem.md) | advanced | DL-26 |
| 29 | DL-P2 | [Project idea: Training Diagnostics Notebook](training-diagnostics/project.md) | ungraded | DL-15, DL-18, DL-20, DL-27 |

# DL-P2 · Project idea: Training Diagnostics Notebook

**Topic:** Deep Learning · ungraded

## Brief

Build a reusable notebook (or script) of experiments that explain why a model trains well or badly:
a learning-rate finder, loss curves for good and bad settings, an overfitting demonstration and
gradient-norm plots. Use it on your digit recogniser or any other model.

## You will use

- DL-15 Optimisers in torch.optim
- DL-18 A Full Training Loop
- DL-20 Dropout with train() and eval()
- DL-27 Debugging Training

## Milestones

1. Write a function that trains a model for a few epochs and returns train and validation losses.
2. Learning-rate finder: increase the learning rate exponentially over one epoch and plot loss against learning rate.
3. Show three curves side by side: learning rate too low, about right and too high.
4. Demonstrate overfitting with a large model on 200 examples, then fix it with dropout or weight decay.
5. Log the gradient norm of every layer per step and show the effect of gradient clipping.

## Stretch goals

- Add a learning-rate schedule (cosine or one-cycle) and compare final accuracy.
- Track experiments in a CSV file and compare runs with different seeds.
- Use TensorBoard to view the curves live.

## Data

Any small classification dataset works: `sklearn.datasets.load_digits()` (bundled) or synthetic data
from `sklearn.datasets.make_moons(n_samples=1000, noise=0.25, random_state=0)`.

## Run it yourself

```bash
pip install torch scikit-learn matplotlib jupyter
jupyter notebook
```

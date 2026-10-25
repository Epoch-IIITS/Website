# DL-P1 · Project idea: Handwritten Digit Recogniser

**Topic:** Deep Learning · ungraded

## Brief

Train a neural network that recognises handwritten digits, then try it on digits you draw
yourself. Start with the small 8×8 digits that ship with scikit-learn, then move to MNIST's 28×28
images.

## You will use

- DL-06 Models with nn.Module
- DL-17 Datasets and DataLoader
- DL-18 A Full Training Loop

## Milestones

1. Load the 8×8 digits with sklearn.datasets.load_digits, scale pixels to [0, 1] and split train/validation/test.
2. Train an MLP with the training loop from the course and plot train and validation loss per epoch.
3. Report test accuracy and a confusion matrix; look at the ten worst mistakes.
4. Switch to MNIST through torchvision and train the same model on 28×28 images.
5. Write a predict(image) function and test it on digits you draw yourself (scaled to the same size).

## Stretch goals

- Add dropout and compare validation curves; save the best model with its state_dict.
- Replace the MLP with a small CNN (see the Computer Vision topic).
- Make a tiny web page or FastAPI endpoint where you draw a digit and get a prediction.

## Data

* 1,797 8×8 digits bundled with scikit-learn (no download):
  [`sklearn.datasets.load_digits`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html).
* MNIST, 70,000 28×28 digits, downloaded by
  [`torchvision.datasets.MNIST`](https://docs.pytorch.org/vision/stable/generated/torchvision.datasets.MNIST.html).

## Run it yourself

```bash
pip install torch torchvision scikit-learn matplotlib
python train_digits.py
```
A CPU is enough: an MLP on MNIST trains in a few minutes.

r"""Reference solution for CV-21 A Small CNN in PyTorch.

Two convolution blocks turn a 16×16 image into 16 feature maps of 4×4; one linear layer maps them to
class scores. Training is the standard loop; scaling pixels to [0, 1] and adding the channel axis
happen in one helper used by both training and prediction.
"""
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class SmallCNN(nn.Module):
    def __init__(self, n_classes=3, size=16):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Linear(16 * (size // 4) ** 2, n_classes)

    def forward(self, x):
        return self.classifier(torch.flatten(self.features(x), 1))


def to_tensor(images):
    return torch.as_tensor(np.asarray(images), dtype=torch.float32)[:, None] / 255


def train_cnn(images, labels, epochs=8, lr=0.01, seed=0):
    X = to_tensor(images)
    y = torch.as_tensor(labels, dtype=torch.long)
    torch.manual_seed(seed)
    model = SmallCNN(int(y.max()) + 1, X.shape[-1])
    loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = []
    for _ in range(epochs):
        model.train()
        total = 0.0
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            total += loss.item() * len(yb)
        history.append(total / len(y))
    model.eval()
    return model, history


def predict(model, images):
    model.eval()
    with torch.no_grad():
        return model(to_tensor(images)).argmax(dim=1).tolist()

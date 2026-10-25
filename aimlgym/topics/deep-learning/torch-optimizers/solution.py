r"""Reference solution for DL-15 Optimisers in torch.optim.

Every optimiser in `torch.optim` updates the tensors it was given when `step()` is called, using
the gradients that `backward()` left in `.grad`. Zeroing first keeps each step's gradient fresh;
recording the loss before the step gives the curve from the starting point.
"""
import torch


def minimise(name, start, lr, steps):
    makers = {
        "sgd": lambda params: torch.optim.SGD(params, lr=lr),
        "momentum": lambda params: torch.optim.SGD(params, lr=lr, momentum=0.9),
        "adam": lambda params: torch.optim.Adam(params, lr=lr),
        "adamw": lambda params: torch.optim.AdamW(params, lr=lr, weight_decay=0.01),
    }
    if name not in makers:
        raise ValueError("unknown optimiser " + str(name))
    p = torch.tensor(start, dtype=torch.float32, requires_grad=True)
    opt = makers[name]([p])
    losses = []
    for _ in range(steps):
        opt.zero_grad()
        loss = (p[0] - 3) ** 2 + 10 * (p[1] + 1) ** 2
        losses.append(loss.item())
        loss.backward()
        opt.step()
    return {"point": p.detach().tolist(), "losses": losses}

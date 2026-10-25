import torch


class Softplus(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        # TODO: save x, return log(1 + e^x) stably
        pass

    @staticmethod
    def backward(ctx, grad_output):
        # TODO
        pass


def softplus(x):
    # TODO
    pass


def passes_gradcheck(fn, shape, seed=0):
    # TODO
    pass

import math


def sigmoid(x):
    # TODO: make this stable for very negative x
    return 1 / (1 + math.exp(-x))


def sigmoid_derivative(x):
    # TODO
    return 0.0


def logit(p):
    # TODO
    return 0.0

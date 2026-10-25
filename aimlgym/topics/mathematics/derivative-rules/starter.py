import math


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    z = math.exp(x)
    return z / (1 + z)


def power_rule(n):
    return (lambda x: x ** n), (lambda x: n * x ** (n - 1))


def sum_rule(f, df, g, dg):
    # TODO
    return f, df


def product_rule(f, df, g, dg):
    # TODO
    return f, df


def chain_rule(f, df, g, dg):
    # TODO
    return f, df


def sigmoid_of_linear(a, b):
    # TODO: use chain_rule
    return sigmoid, sigmoid

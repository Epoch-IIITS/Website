r"""Reference solution for MA-11 Derivative Rules and the Chain Rule.

Every rule is a direct translation of its formula into a pair of closures. Because rules accept
and return pairs, they compose: `sigmoid_of_linear` is one call to `chain_rule`, and the tests
build larger expressions (products of chains) the same way and confirm them numerically.
"""
import math


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    z = math.exp(x)
    return z / (1 + z)


def power_rule(n):
    return (lambda x: x ** n), (lambda x: n * x ** (n - 1))


def sum_rule(f, df, g, dg):
    return (lambda x: f(x) + g(x)), (lambda x: df(x) + dg(x))


def product_rule(f, df, g, dg):
    return (lambda x: f(x) * g(x)), (lambda x: df(x) * g(x) + f(x) * dg(x))


def chain_rule(f, df, g, dg):
    return (lambda x: f(g(x))), (lambda x: df(g(x)) * dg(x))


def sigmoid_of_linear(a, b):
    dsigmoid = lambda u: sigmoid(u) * (1 - sigmoid(u))
    return chain_rule(sigmoid, dsigmoid, lambda x: a * x + b, lambda x: a)

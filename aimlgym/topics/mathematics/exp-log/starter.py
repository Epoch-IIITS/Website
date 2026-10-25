import math


def log_base(x, base):
    # TODO
    return 0.0


def doubling_time(rate):
    # TODO
    return 0.0


def log_likelihood(probs):
    # TODO: sum of logs, with validation
    return math.log(math.prod(probs))


def logsumexp(values):
    # TODO: subtract the maximum first
    return math.log(sum(math.exp(v) for v in values))

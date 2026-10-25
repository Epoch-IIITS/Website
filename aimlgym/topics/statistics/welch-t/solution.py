r"""Reference solution for ST-18 Welch's t-statistic by Hand.

Each group's squared standard error of the mean is its sample variance over its size. Their sum
is the variance of the difference in means; t divides the observed difference by its square
root. The Welch–Satterthwaite formula combines the two contributions into an effective df.
"""
import math


def _mean_var(a):
    n = len(a)
    if n < 2:
        raise ValueError("each sample needs at least two values")
    m = sum(a) / n
    return m, sum((v - m) ** 2 for v in a) / (n - 1), n


def welch_t(x, y):
    mx, sx2, nx = _mean_var(x)
    my, sy2, ny = _mean_var(y)
    vx, vy = sx2 / nx, sy2 / ny
    if vx + vy == 0:
        raise ValueError("both samples have zero variance")
    t = (mx - my) / math.sqrt(vx + vy)
    df = (vx + vy) ** 2 / (vx ** 2 / (nx - 1) + vy ** 2 / (ny - 1))
    return t, df

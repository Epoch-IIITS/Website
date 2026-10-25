r"""Reference solution for ST-14 Introducing scipy.stats.

The frozen distribution holds the parameters, so every fact is one method call. Only the density
method differs between continuous (`pdf`) and discrete (`pmf`) families. Validation happens before
SciPy is called, because SciPy returns `nan` for invalid parameters instead of raising.
"""
from scipy import stats


def distribution_facts(kind, params, x, q):
    if not 0 < q < 1:
        raise ValueError("q must be strictly between 0 and 1")
    if kind == "norm":
        mu, sigma = params
        if sigma <= 0:
            raise ValueError("sigma must be positive")
        dist = stats.norm(loc=mu, scale=sigma)
        density = dist.pdf(x)
    elif kind == "binom":
        n, p = params
        if n < 0 or not 0 <= p <= 1:
            raise ValueError("need n >= 0 and 0 <= p <= 1")
        dist = stats.binom(n, p)
        density = dist.pmf(x)
    else:
        raise ValueError("kind must be 'norm' or 'binom'")
    return {"density": float(density), "cdf": float(dist.cdf(x)), "quantile": float(dist.ppf(q)),
            "mean": float(dist.mean()), "std": float(dist.std())}

import numpy as np


def score_estimates(d, n, rng, baseline=False):
    """Score-function estimates of d/d mu_1 E|x|^2 at mu = 0."""
    X = rng.standard_normal((n, d))
    f = np.sum(X * X, axis=1)
    return (f - (d if baseline else 0.0)) * X[:, 0]


def reparam_estimates(d, n, rng):
    """Pathwise estimates 2 x_1 at mu = 0."""
    return 2 * rng.standard_normal(n)


def variance_table(ds, n, rng):
    """Sample variances of the three estimators for each dimension."""
    return {d: (float(np.var(score_estimates(d, n, rng))), float(np.var(score_estimates(d, n, rng, True))), float(np.var(reparam_estimates(d, n, rng)))) for d in ds}


def theory(d):
    """Exact per-sample variances at mu = 0."""
    return (d + 2) * (d + 4), 2 * d + 8, 4

import numpy as np


def score_estimates(d, n, rng, baseline=False):
    """Score-function estimates of d/d mu_1 E|x|^2 at mu = 0."""
    raise NotImplementedError


def reparam_estimates(d, n, rng):
    """Pathwise estimates 2 x_1 at mu = 0."""
    raise NotImplementedError


def variance_table(ds, n, rng):
    """Sample variances of the three estimators for each dimension."""
    raise NotImplementedError


def theory(d):
    """Exact per-sample variances at mu = 0."""
    raise NotImplementedError

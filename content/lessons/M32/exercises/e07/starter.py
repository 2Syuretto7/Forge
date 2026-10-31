import math
import numpy as np


def gibbs_bivariate(rho, n, rng):
    """Gibbs sampler for the standard bivariate normal with correlation rho."""
    raise NotImplementedError


def lag1(x):
    """Lag-one autocorrelation."""
    raise NotImplementedError


def gibbs_gaussian(mu, cov, n, rng):
    """Systematic-scan Gibbs sampler for N(mu, cov)."""
    raise NotImplementedError

import math
import numpy as np


def autocorr(x, max_lag):
    """Autocorrelations at lags 0..max_lag by the FFT."""
    raise NotImplementedError


def ess(x):
    """Effective sample size with pairwise truncation."""
    raise NotImplementedError


def mcse(x):
    """Monte Carlo standard error of the mean."""
    raise NotImplementedError


def ar1(phi, n, rng):
    """AR(1) chain with unit stationary variance."""
    raise NotImplementedError

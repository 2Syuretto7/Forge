import numpy as np


def spectrum(kappa, d=1000):
    """Eigenvalues spread log-uniformly from 1 to kappa."""
    raise NotImplementedError


def run_iterations(kappa, eps=1e-6, d=1000):
    """Gradient-descent steps on the diagonal quadratic to relative error eps."""
    raise NotImplementedError


def _err(k, logr, d):
    raise NotImplementedError


def predict_iterations(kappa, eps=1e-6, d=1000):
    """The same count from the eigenvalues alone."""
    raise NotImplementedError


def slope(kappas, counts):
    """Slope of log(count) against log(kappa)."""
    raise NotImplementedError

import numpy as np


def midpoint_errors(ns):
    """Midpoint-rule errors for x^(-1/2) on [0, 1]."""
    raise NotImplementedError


def fitted_order(ns, errs):
    """Least-squares slope of -log(error) against log n."""
    raise NotImplementedError


def after_substitution(n):
    """Simpson error on the substituted, constant integrand."""
    raise NotImplementedError

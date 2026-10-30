import numpy as np


def _simp(f, a, b, n):
    raise NotImplementedError


def simpson_step_errors(ns):
    """Simpson errors for the step at 1/3."""
    raise NotImplementedError


def fitted_order(ns, errs):
    """Least-squares slope of -log(error) against log n."""
    raise NotImplementedError


def split_at_jump(n):
    """Error after splitting at the jump."""
    raise NotImplementedError

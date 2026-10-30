import math


def errors(history, root):
    """|x_k - r|."""
    raise NotImplementedError


def _usable(errs):
    raise NotImplementedError


def orders(errs):
    """Order estimates from consecutive triples."""
    raise NotImplementedError


def rates(errs):
    """Ratios of consecutive errors."""
    raise NotImplementedError


def classify(errs):
    """linear, superlinear or quadratic."""
    raise NotImplementedError

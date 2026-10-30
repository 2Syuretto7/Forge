import numpy as np


def fit_alpha(X, y, alpha):
    """Log word probabilities with smoothing alpha."""
    raise NotImplementedError


def log_odds_alpha(X, y, x, alpha):
    """Log-odds with equal priors."""
    raise NotImplementedError


def veto(X, y, x):
    """Infinite or undefined without smoothing, finite with it."""
    raise NotImplementedError

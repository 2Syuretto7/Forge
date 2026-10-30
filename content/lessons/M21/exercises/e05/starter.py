import numpy as np


def fit(X, y, alpha=1.0):
    """Smoothed class priors and word log-probabilities."""
    raise NotImplementedError


def log_odds(model, X):
    """log P(1 | doc) - log P(0 | doc) for each row."""
    raise NotImplementedError


def predict_proba(model, X):
    """Probability of class 1."""
    raise NotImplementedError

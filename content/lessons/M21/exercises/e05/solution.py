import numpy as np


def fit(X, y, alpha=1.0):
    """Smoothed class priors and word log-probabilities."""
    prior = np.array([np.mean(y == 0), np.mean(y == 1)])
    counts = np.vstack([X[y == c].sum(axis=0) + alpha for c in (0, 1)]).astype(float)
    return {"log_prior": np.log(prior), "log_word": np.log(counts / counts.sum(axis=1, keepdims=True))}


def log_odds(model, X):
    """log P(1 | doc) - log P(0 | doc) for each row."""
    lp, lw = model["log_prior"], model["log_word"]
    return lp[1] - lp[0] + X @ (lw[1] - lw[0])


def predict_proba(model, X):
    """Probability of class 1."""
    z = np.clip(log_odds(model, X), -700, 700)
    return 1 / (1 + np.exp(-z))

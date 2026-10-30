import numpy as np


# provided
def fit(X, y, alpha=1.0):
    prior = np.array([np.mean(y == 0), np.mean(y == 1)])
    counts = np.vstack([X[y == c].sum(axis=0) + alpha for c in (0, 1)]).astype(float)
    return {"log_prior": np.log(prior), "log_word": np.log(counts / counts.sum(axis=1, keepdims=True))}


def word_scores(model):
    """log P(w | 1) - log P(w | 0)."""
    raise NotImplementedError


def log_odds_counts(model, counts):
    """Log-odds of a (possibly fractional) count vector."""
    raise NotImplementedError


def top_words(model, k):
    """Indices of the k highest scores."""
    raise NotImplementedError

import numpy as np


# provided
def make_corpus(n_docs=20000, seed=0, V=300):
    rng = np.random.default_rng(seed)
    base = rng.dirichlet(np.full(V, 0.3))
    tilt = np.exp(rng.normal(0, 0.6, V))
    p_spam = base * tilt / np.sum(base * tilt)
    p_ham = base / tilt / np.sum(base / tilt)
    y = (rng.random(n_docs) < 1 / 3).astype(int)
    lengths = rng.poisson(16, n_docs) + 4
    X = np.where(y[:, None] == 1, rng.multinomial(lengths, p_spam), rng.multinomial(lengths, p_ham))
    for words in ((5, 6, 7, 8), (20, 21, 22, 23), (40, 41, 42, 43)):
        show = np.where(y == 1, rng.random(n_docs) < 0.35, rng.random(n_docs) < 0.04)
        X[:, list(words)] += 2 * show[:, None]
    return X, y


def fit(X, y, alpha=1.0):
    """Smoothed naive Bayes."""
    raise NotImplementedError


def log_odds(model, X):
    """Log-odds of class 1 per row."""
    raise NotImplementedError


def split(X, y):
    """12,000 train, 4,000 calibration, 4,000 test."""
    raise NotImplementedError


def _sig(z):
    raise NotImplementedError


def ece(p, y, bins=10):
    """Expected calibration error."""
    raise NotImplementedError


def fit_temperature(z, y):
    """Minimize the NLL over T by bisection on its derivative."""
    raise NotImplementedError


def report(seed=0):
    """Accuracy, calibration before and after, and the temperature."""
    raise NotImplementedError


# your answer
NOTE = """
"""

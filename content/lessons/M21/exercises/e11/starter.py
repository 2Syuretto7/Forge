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


# provided
def nb_probabilities(seed=0):
    X, y = make_corpus(seed=seed)
    Xtr, ytr, Xte, yte = X[:16000], y[:16000], X[16000:], y[16000:]
    prior = np.array([np.mean(ytr == 0), np.mean(ytr == 1)])
    counts = np.vstack([Xtr[ytr == c].sum(axis=0) + 1.0 for c in (0, 1)])
    lw = np.log(counts / counts.sum(axis=1, keepdims=True))
    z = np.clip(np.log(prior[1] / prior[0]) + Xte @ (lw[1] - lw[0]), -700, 700)
    return 1 / (1 + np.exp(-z)), yte


def reliability(p, y, bins=10):
    """(mean predicted, observed frequency, count) per non-empty bin."""
    raise NotImplementedError


def ece(p, y, bins=10):
    """Expected calibration error."""
    raise NotImplementedError


def overconfidence(p, y, bins=10):
    """Average gap above 1/2."""
    raise NotImplementedError

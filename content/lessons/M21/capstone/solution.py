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
    prior = np.array([np.mean(y == 0), np.mean(y == 1)])
    counts = np.vstack([X[y == c].sum(axis=0) + alpha for c in (0, 1)]).astype(float)
    return {"log_prior": np.log(prior), "log_word": np.log(counts / counts.sum(axis=1, keepdims=True))}


def log_odds(model, X):
    """Log-odds of class 1 per row."""
    lp, lw = model["log_prior"], model["log_word"]
    return lp[1] - lp[0] + X @ (lw[1] - lw[0])


def split(X, y):
    """12,000 train, 4,000 calibration, 4,000 test."""
    return (X[:12000], y[:12000]), (X[12000:16000], y[12000:16000]), (X[16000:], y[16000:])


def _sig(z):
    return 1 / (1 + np.exp(-np.clip(z, -700, 700)))


def ece(p, y, bins=10):
    """Expected calibration error."""
    idx = np.minimum((p * bins).astype(int), bins - 1)
    total = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            total += m.mean() * abs(p[m].mean() - y[m].mean())
    return float(total)


def fit_temperature(z, y):
    """Minimize the NLL over T by bisection on its derivative."""
    lo, hi = 0.25, 10.0
    for _ in range(60):
        T = (lo + hi) / 2
        if np.mean((_sig(z / T) - y) * (-z / T ** 2)) < 0:
            lo = T
        else:
            hi = T
    return (lo + hi) / 2


def report(seed=0):
    """Accuracy, calibration before and after, and the temperature."""
    X, y = make_corpus(seed=seed)
    (Xtr, ytr), (Xca, yca), (Xte, yte) = split(X, y)
    m = fit(Xtr, ytr)
    T = fit_temperature(log_odds(m, Xca), yca)
    z = log_odds(m, Xte)
    return {
        "accuracy": float(np.mean((z > 0) == (yte == 1))),
        "ece_before": ece(_sig(z), yte),
        "ece_after": ece(_sig(z / T), yte),
        "temperature": float(T),
    }


# your answer
NOTE = """
The independence assumption fails for the three phrases: in spam their four words appear
together, so a message containing a phrase gives naive Bayes four pieces of evidence that are
really one. Its log-odds are too large in magnitude, and it is overconfident. The fitted
temperature, well above 1, measures that excess: dividing the log-odds by it pulls the
probabilities back toward one half and brings the calibration error down. Calibration changes
the confidence attached to each prediction, but not the predictions themselves: the sign of the
log-odds, and so every decision at threshold one half, stays the same.
"""

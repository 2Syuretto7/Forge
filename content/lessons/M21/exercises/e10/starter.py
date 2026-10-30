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
def fit(X, y, alpha=1.0):
    prior = np.array([np.mean(y == 0), np.mean(y == 1)])
    counts = np.vstack([X[y == c].sum(axis=0) + alpha for c in (0, 1)]).astype(float)
    return {"log_prior": np.log(prior), "log_word": np.log(counts / counts.sum(axis=1, keepdims=True))}


# provided
def predict_proba(model, X):
    lp, lw = model["log_prior"], model["log_word"]
    z = np.clip(lp[1] - lp[0] + X @ (lw[1] - lw[0]), -700, 700)
    return 1 / (1 + np.exp(-z))


def train_test(X, y, n_train):
    """Split by position."""
    raise NotImplementedError


def accuracy(model, X, y):
    """Fraction correct at threshold 1/2."""
    raise NotImplementedError


def evaluate(seed=0):
    """Test accuracy of naive Bayes trained on 16,000 messages."""
    raise NotImplementedError

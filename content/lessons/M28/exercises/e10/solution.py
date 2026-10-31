import numpy as np


def log_partition(theta):
    """log sum exp(theta)."""
    t = np.asarray(theta, dtype=float)
    m = t.max()
    return float(m + np.log(np.sum(np.exp(t - m))))


def grad_log_partition(theta):
    """Gradient of the log-partition: the softmax."""
    t = np.asarray(theta, dtype=float)
    return np.exp(t - log_partition(t))


def nll(theta, counts):
    """Negative log-likelihood of category counts."""
    c = np.asarray(counts, dtype=float)
    return float(c.sum() * log_partition(theta) - c @ np.asarray(theta, dtype=float))


def fit(counts, steps=500, lr=1.0):
    """Gradient descent on the average negative log-likelihood."""
    c = np.asarray(counts, dtype=float)
    theta = np.zeros(len(c))
    for _ in range(steps):
        theta -= lr * (grad_log_partition(theta) - c / c.sum())
    return theta

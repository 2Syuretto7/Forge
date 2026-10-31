import math
import numpy as np


def logsumexp(z):
    """Stable log-sum-exp along the last axis."""
    z = np.asarray(z, dtype=float)
    m = np.max(z, axis=-1, keepdims=True)
    m = np.where(np.isfinite(m), m, 0.0)
    with np.errstate(divide="ignore"):
        out = m + np.log(np.sum(np.exp(z - m), axis=-1, keepdims=True))
    return out[..., 0] if out.ndim > 1 else float(out[0])


def log_softmax(z):
    """Stable log-softmax along the last axis."""
    z = np.asarray(z, dtype=float)
    return z - np.expand_dims(np.asarray(logsumexp(z)), -1)


def softmax(z):
    """Stable softmax along the last axis."""
    return np.exp(log_softmax(z))


def sigmoid(x):
    """Stable sigmoid."""
    x = np.asarray(x, dtype=float)
    e = np.exp(-np.abs(x))
    return np.where(x >= 0, 1 / (1 + e), e / (1 + e))


def softplus(x):
    """Stable log(1 + e^x)."""
    x = np.asarray(x, dtype=float)
    return np.maximum(x, 0) + np.log1p(np.exp(-np.abs(x)))


def log_sigmoid(x):
    """Stable log(sigmoid(x))."""
    return -softplus(-np.asarray(x, dtype=float))


def cross_entropy(logits, labels):
    """Mean cross-entropy of a batch of logit rows."""
    ls = log_softmax(np.atleast_2d(logits))
    labels = np.asarray(labels)
    return float(-np.mean(ls[np.arange(len(labels)), labels]))


def bce_with_logits(x, y):
    """Binary cross-entropy from logits."""
    x = np.asarray(x, dtype=float)
    return np.maximum(x, 0) - x * y + np.log1p(np.exp(-np.abs(x)))


def mean_var(x):
    """Mean and variance (n - 1) by two passes."""
    x = np.asarray(x, dtype=float)
    m = x.sum() / len(x)
    d = x - m
    return float(m), float(np.sum(d * d) / (len(x) - 1))


def log1mexp(a):
    """log(1 - e^-a) for a > 0."""
    return math.log(-math.expm1(-a)) if a < math.log(2) else math.log1p(-math.exp(-a))


def compensated_sum(x):
    """Neumaier summation."""
    s, c = 0.0, 0.0
    for v in np.asarray(x, dtype=float).tolist():
        t = s + v
        c += (s - t) + v if abs(s) >= abs(v) else (v - t) + s
        s = t
    return s + c

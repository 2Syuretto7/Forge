import math
import numpy as np


def sigmoid(t):
    """Logistic function."""
    return 1 / (1 + math.exp(-t))


def log_prob(x, theta):
    """log p_theta(x) for x in {0, 1}."""
    p = sigmoid(theta)
    return math.log(p) if x == 1 else math.log(1 - p)


def score(x, theta):
    """Derivative of log p_theta(x) in theta."""
    return x - sigmoid(theta)


def exact_grad(theta, r1, r0):
    """Gradient of the expected reward."""
    p = sigmoid(theta)
    return (r1 - r0) * p * (1 - p)


def estimate_grad(theta, r1, r0, n, rng):
    """Score-function estimate of the gradient."""
    p = sigmoid(theta)
    x = (rng.random(n) < p).astype(float)
    r = np.where(x == 1, r1, r0)
    return float(np.mean(r * (x - p)))

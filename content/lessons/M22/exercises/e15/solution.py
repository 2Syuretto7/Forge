import numpy as np


def plug_in(g, values, probs):
    """g(E[X])."""
    return float(g(np.sum(np.asarray(values, dtype=float) * np.asarray(probs, dtype=float))))


def expect(g, values, probs):
    """E[g(X)]."""
    return float(np.sum(g(np.asarray(values, dtype=float)) * np.asarray(probs, dtype=float)))


def mc_expect(g, samples):
    """Monte Carlo estimate of E[g(X)]."""
    return float(np.mean(g(np.asarray(samples, dtype=float))))


def relu_second_moment():
    """E[max(Z, 0)^2] for a standard normal Z."""
    return 0.5

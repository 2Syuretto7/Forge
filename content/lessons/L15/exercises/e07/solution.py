import numpy as np


def isoflop_minimum(N, L):
    """Runs at one compute budget: fit a parabola to loss against log N and return the model size
    at its vertex and the loss there."""
    c2, c1, c0 = np.polyfit(np.log(N), L, 2)
    x = -c1 / (2 * c2)
    return np.exp(x), c0 + c1 * x + c2 * x * x


def allocation_exponent(C, N_opt):
    """The exponent a in N_opt = k C^a, by a least-squares line in log-log coordinates."""
    return np.polyfit(np.log(C), np.log(N_opt), 1)[0]

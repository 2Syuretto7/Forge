import numpy as np


# provided
def log_odds(model, x):
    lp, lw = model["log_prior"], model["log_word"]
    return float(lp[1] - lp[0] + np.asarray(x, dtype=float) @ (lw[1] - lw[0]))


def doubled_log_odds(model, x):
    """Log-odds of the doubled counts."""
    return log_odds(model, 2 * np.asarray(x))


def prior_free_part(model, x):
    """Word contribution to the log-odds."""
    lp = model["log_prior"]
    return log_odds(model, x) - float(lp[1] - lp[0])


def confidence_after_duplication(model, x):
    """(P(1 | x), P(1 | 2x))."""
    s = lambda v: 1 / (1 + np.exp(-v))  # noqa: E731
    return float(s(log_odds(model, x))), float(s(doubled_log_odds(model, x)))

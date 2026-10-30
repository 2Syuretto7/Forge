import numpy as np


def fit_alpha(X, y, alpha):
    """Log word probabilities with smoothing alpha."""
    counts = np.vstack([X[y == c].sum(axis=0) + alpha for c in (0, 1)]).astype(float)
    with np.errstate(divide="ignore"):
        return np.log(counts / counts.sum(axis=1, keepdims=True))


def log_odds_alpha(X, y, x, alpha):
    """Log-odds with equal priors."""
    lw = fit_alpha(X, y, alpha)
    with np.errstate(invalid="ignore"):
        d = lw[1] - lw[0]
        return float(np.sum(np.where(np.asarray(x) > 0, np.asarray(x) * d, 0.0)))


def veto(X, y, x):
    """Infinite or undefined without smoothing, finite with it."""
    return (not np.isfinite(log_odds_alpha(X, y, x, 0.0))) and np.isfinite(log_odds_alpha(X, y, x, 1.0))

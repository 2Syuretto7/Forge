import numpy as np

D = 200
N = 20
MAXP = 80


def make_problem(seed, noise=0.3):
    """Returns X (N, D), y (N,), beta (D,), lam_x (D,), W (MAXP, D). Do not change."""
    rng = np.random.default_rng(seed)
    lam_x = np.arange(1, D + 1) ** -1.5
    beta = rng.normal(size=D) * np.sqrt(lam_x)
    beta /= np.sqrt(np.sum(lam_x * beta ** 2))
    X = rng.normal(size=(N, D)) * np.sqrt(lam_x)
    y = X @ beta + noise * rng.normal(size=N)
    W = rng.normal(size=(MAXP, D))
    return X, y, beta, lam_x, W


def fit(Phi, y, lam):
    raise NotImplementedError


def excess_risk(w, W_p, beta, lam_x):
    raise NotImplementedError


def curve(ps, lam=0.0, seeds=range(10), noise=0.3):
    """Return (risks, sigma_mins), arrays aligned with ps."""
    raise NotImplementedError


def peak(ps, risks):
    raise NotImplementedError


REPORT = """
"""

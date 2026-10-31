import numpy as np


def model(theta, x):
    """E + A x^(-alpha)."""
    E, A, alpha = theta
    return E + A * np.asarray(x, dtype=float) ** (-alpha)


def jacobian(theta, x):
    """Derivatives of the model in E, A and alpha."""
    _, A, alpha = theta
    x = np.asarray(x, dtype=float)
    p = x ** (-alpha)
    return np.stack([np.ones_like(x), p, -A * p * np.log(x)], axis=1)


def fit(x, y, theta0, iters=60):
    """Levenberg-Marquardt fit."""
    theta = np.array(theta0, dtype=float)
    r = y - model(theta, x)
    loss, lam = r @ r, 1e-2
    for _ in range(iters):
        J = jacobian(theta, x)
        G = J.T @ J
        new = theta + np.linalg.solve(G + lam * np.diag(np.diag(G)), J.T @ r)
        rn = y - model(new, x)
        if rn @ rn < loss:
            theta, r, loss, lam = new, rn, rn @ rn, lam / 3
        else:
            lam *= 3
    return theta


def residual_bootstrap(x, y, theta_hat, B, rng):
    """Refits on datasets built from resampled residuals."""
    fitted = model(theta_hat, x)
    res = y - fitted
    return np.array([fit(x, fitted + rng.choice(res, size=len(x), replace=True), theta_hat) for _ in range(B)])


def percentile_interval(samples, level=0.95):
    """Percentile interval of each column."""
    lo, hi = np.quantile(samples, [(1 - level) / 2, (1 + level) / 2], axis=0)
    return lo, hi

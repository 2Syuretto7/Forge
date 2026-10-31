import numpy as np


def fit_loglog(x, y):
    """(A, alpha) from least squares on the logarithms."""
    slope, intercept = np.polyfit(np.log(x), np.log(y), 1)
    return float(np.exp(intercept)), float(-slope)


def _model(theta, x):
    return theta[0] + theta[1] * np.asarray(x, dtype=float) ** (-theta[2])


def fit_with_floor(x, y, theta0, iters=100):
    """Levenberg-Marquardt fit of E + A x^(-alpha)."""
    theta = np.array(theta0, dtype=float)
    r = y - _model(theta, x)
    loss, lam = r @ r, 1e-2
    for _ in range(iters):
        p = x ** (-theta[2])
        J = np.stack([np.ones_like(x), p, -theta[1] * p * np.log(x)], axis=1)
        G = J.T @ J
        new = theta + np.linalg.solve(G + lam * np.diag(np.diag(G)), J.T @ r)
        with np.errstate(all="ignore"):
            rn = y - _model(new, x)
            ln = rn @ rn
        if np.isfinite(ln) and ln < loss:
            theta, r, loss, lam = new, rn, ln, lam / 3
        else:
            lam *= 3
    return theta


def extrapolation_errors(x, y, x0, truth):
    """Relative errors of the log-log line and the floor fit at x0."""
    A, alpha = fit_loglog(x, y)
    th = fit_with_floor(x, y, [np.min(y) * 0.9, 1.0, 0.5])
    return A * x0 ** (-alpha) / truth - 1, float(_model(th, x0)) / truth - 1

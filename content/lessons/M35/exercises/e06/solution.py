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


def fit(x, y, theta0, iters=100):
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


def param_cov(x, y, theta):
    """s^2 (J^T J)^(-1)."""
    r = y - model(theta, x)
    J = jacobian(theta, x)
    s2 = (r @ r) / (len(x) - len(theta))
    return s2 * np.linalg.inv(J.T @ J)


def standard_errors(x, y, theta):
    """Standard errors of the fitted parameters."""
    return np.sqrt(np.diag(param_cov(x, y, theta)))

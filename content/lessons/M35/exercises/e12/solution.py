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


def extrapolation_trial(x, theta_true, sigma, x0s, rng):
    """Prediction errors and delta-method standard errors at x0s for one dataset."""
    y = model(theta_true, x) + sigma * rng.standard_normal(len(x))
    th = fit(x, y, theta_true)
    r = y - model(th, x)
    J = jacobian(th, x)
    cov = (r @ r) / (len(x) - 3) * np.linalg.inv(J.T @ J)
    G = jacobian(th, x0s)
    se = np.sqrt(np.einsum("ij,jk,ik->i", G, cov, G))
    return model(th, x0s) - model(theta_true, x0s), se


def coverage(errors, ses, z=1.96):
    """Fraction of trials whose error lies inside the band."""
    return np.mean(np.abs(np.asarray(errors)) <= z * np.asarray(ses), axis=0)


def rms_error(errors):
    """Root-mean-square error per column."""
    return np.sqrt(np.mean(np.asarray(errors) ** 2, axis=0))

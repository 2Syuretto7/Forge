import numpy as np


def broken_law(x, E=1.7, A=2.0, a1=0.5, a2=0.2, xb=1e3):
    """A power law whose exponent changes at xb."""
    x = np.asarray(x, dtype=float)
    return np.where(x <= xb, E + A * x ** (-a1), E + A * xb ** (-a1) * (x / xb) ** (-a2))


def _model(theta, x):
    return theta[0] + theta[1] * np.asarray(x, dtype=float) ** (-theta[2])


def _jac(theta, x):
    p = np.asarray(x, dtype=float) ** (-theta[2])
    return np.stack([np.ones_like(p), p, -theta[1] * p * np.log(x)], axis=-1)


def fit_and_band(x, y, x0, z=1.96, iters=100):
    """Prediction and delta-method half-width at x0."""
    theta = np.array([1.5, 1.5, 0.4])
    r = y - _model(theta, x)
    loss, lam = r @ r, 1e-2
    for _ in range(iters):
        J = _jac(theta, x)
        G = J.T @ J
        new = theta + np.linalg.solve(G + lam * np.diag(np.diag(G)), J.T @ r)
        rn = y - _model(new, x)
        if rn @ rn < loss:
            theta, r, loss, lam = new, rn, rn @ rn, lam / 3
        else:
            lam *= 3
    J = _jac(theta, x)
    cov = loss / (len(x) - 3) * np.linalg.inv(J.T @ J)
    g = _jac(theta, np.array([x0]))[0]
    return float(_model(theta, x0)), float(z * np.sqrt(g @ cov @ g))


def inside(pred, half, truth):
    """Whether the truth lies in the band."""
    return bool(abs(pred - truth) <= half)

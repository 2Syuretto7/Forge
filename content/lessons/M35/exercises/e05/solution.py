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


def sse(theta, x, y):
    """Sum of squared residuals, infinite when not finite."""
    with np.errstate(all="ignore"):
        r = y - model(theta, x)
        v = float(r @ r)
    return v if np.isfinite(v) else np.inf


def levenberg_marquardt(x, y, theta0, lam=1e-2, iters=200):
    """Damped Gauss-Newton with an adaptive damping parameter."""
    theta = np.array(theta0, dtype=float)
    loss = sse(theta, x, y)
    history = [loss]
    for _ in range(iters):
        J = jacobian(theta, x)
        G = J.T @ J
        g = J.T @ (y - model(theta, x))
        step = np.linalg.solve(G + lam * np.diag(np.diag(G)), g)
        new = theta + step
        new_loss = sse(new, x, y)
        if new_loss < loss:
            theta, loss, lam = new, new_loss, lam / 3
            history.append(loss)
        else:
            lam *= 3
    return theta, history


def gauss_newton(x, y, theta0, iters=50):
    """Undamped Gauss-Newton, stopping at the first non-finite value."""
    theta = np.array(theta0, dtype=float)
    with np.errstate(all="ignore"):
        for _ in range(iters):
            r = y - model(theta, x)
            J = jacobian(theta, x)
            if not (np.all(np.isfinite(r)) and np.all(np.isfinite(J))):
                break
            new = theta + np.linalg.lstsq(J, r, rcond=None)[0]
            if not np.all(np.isfinite(new)):
                break
            theta = new
    return theta

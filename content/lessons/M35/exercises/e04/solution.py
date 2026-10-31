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


def gauss_newton(x, y, theta0, iters=50):
    """Gauss-Newton iterations for the power law with a floor."""
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

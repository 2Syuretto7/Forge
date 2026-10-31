import numpy as np

N0, D0 = 1e9, 1e10


def surface(theta, N, D):
    """E + exp(a - alpha u) + exp(b - beta v)."""
    E, a, alpha, b, beta = theta
    u, v = np.log(np.asarray(N) / N0), np.log(np.asarray(D) / D0)
    return E + np.exp(a - alpha * u) + np.exp(b - beta * v)


def grad_surface(theta, N, D):
    """Jacobian of the surface in (E, a, alpha, b, beta)."""
    E, a, alpha, b, beta = theta
    u, v = np.log(np.asarray(N) / N0), np.log(np.asarray(D) / D0)
    tn, td = np.exp(a - alpha * u), np.exp(b - beta * v)
    return np.stack([np.ones_like(u), tn, -u * tn, td, -v * td], axis=1)


def fit_surface(N, D, L, theta0, iters=200):
    """Levenberg-Marquardt fit of the loss surface."""
    theta = np.array(theta0, dtype=float)
    r = L - surface(theta, N, D)
    loss, lam = r @ r, 1e-2
    for _ in range(iters):
        J = grad_surface(theta, N, D)
        G = J.T @ J
        new = theta + np.linalg.solve(G + lam * np.diag(np.diag(G)), J.T @ r)
        with np.errstate(all="ignore"):
            rn = L - surface(new, N, D)
            ln = rn @ rn
        if np.isfinite(ln) and ln < loss:
            theta, r, loss, lam = new, rn, ln, lam / 3
        else:
            lam *= 3
    return theta


def to_chinchilla(theta):
    """(E, A, alpha, B, beta) in the original parametrization."""
    E, a, alpha, b, beta = theta
    return E, float(np.exp(a) * N0**alpha), alpha, float(np.exp(b) * D0**beta), beta

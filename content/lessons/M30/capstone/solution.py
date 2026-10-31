import numpy as np


# provided
def make_data(n=400, seed=0):
    rng = np.random.default_rng(seed)
    Z = rng.normal(size=(n, 4))
    y = np.sign(Z @ np.array([1.0, -1.0, 0.5, 2.0]) + 0.7 + 0.5 * rng.normal(size=n))
    return np.hstack([Z, np.ones((n, 1))]), y


def _G(alpha, X, y):
    return y * (X @ (X.T @ (alpha * y))) - 1


def kkt_residual(alpha, X, y, C):
    """Largest projected-gradient violation of the dual."""
    G = _G(alpha, X, y)
    eps = 1e-12
    inner = (alpha > eps) & (alpha < C - eps)
    at0 = alpha <= eps
    v = np.where(inner, np.abs(G), np.where(at0, np.maximum(0, -G), np.maximum(0, G)))
    return float(v.max())


def duality_gap(alpha, X, y, C):
    """Relative duality gap."""
    w = X.T @ (alpha * y)
    P = 0.5 * w @ w + C * np.sum(np.maximum(0, 1 - y * (X @ w)))
    D = alpha.sum() - 0.5 * w @ w
    return float((P - D) / P)


def solve(X, y, C, tol=1e-5, max_epochs=500, seed=0):
    """Dual coordinate ascent until the KKT residual is at most tol."""
    rng = np.random.default_rng(seed)
    n = len(y)
    alpha = np.zeros(n)
    w = np.zeros(X.shape[1])
    sq = np.sum(X * X, axis=1)
    for _ in range(max_epochs):
        for i in rng.permutation(n):
            G = y[i] * (w @ X[i]) - 1
            new = min(max(alpha[i] - G / sq[i], 0.0), C)
            if new != alpha[i]:
                w += (new - alpha[i]) * y[i] * X[i]
                alpha[i] = new
        if kkt_residual(alpha, X, y, C) <= tol:
            break
    return alpha, w


def kl_optimum(pi, r, beta):
    """pi exp(r / beta), normalized."""
    z = np.log(np.asarray(pi, dtype=float)) + np.asarray(r, dtype=float) / beta
    e = np.exp(z - z.max())
    return e / e.sum()


def _objective(p, pi, r, beta):
    m = p > 0
    return float(p @ r - beta * np.sum(p[m] * np.log(p[m] / pi[m])))


def check_kl_optimum(pi, r, beta, trials, rng):
    """Largest improvement any random distribution makes over kl_optimum."""
    pi, r = np.asarray(pi, dtype=float), np.asarray(r, dtype=float)
    best = _objective(kl_optimum(pi, r, beta), pi, r, beta)
    return max(_objective(rng.dirichlet(np.ones(len(pi))), pi, r, beta) - best for _ in range(trials))


def log_ratio_slope(pi, r, beta):
    """Slope of log(p / pi) against r."""
    p = kl_optimum(pi, r, beta)
    return float(np.polyfit(np.asarray(r, dtype=float), np.log(p / np.asarray(pi, dtype=float)), 1)[0])

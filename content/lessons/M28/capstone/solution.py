import math
import numpy as np


def quadratic(eigs, seed):
    """Symmetric matrix with the given eigenvalues and random eigenvectors."""
    d = len(eigs)
    Q, _ = np.linalg.qr(np.random.default_rng(seed).standard_normal((d, d)))
    return Q @ np.diag(eigs) @ Q.T


def gd_iterations(A, x0, step, eps=1e-6, max_iter=200000):
    """Gradient-descent iterations to relative error eps."""
    x = np.array(x0, dtype=float)
    target = eps * np.linalg.norm(x)
    for k in range(max_iter + 1):
        if np.linalg.norm(x) <= target:
            return k
        x = x - step * (A @ x)
    return max_iter


def predicted_iterations(A, x0, step, eps=1e-6):
    """Iterations from the eigendecomposition alone."""
    lam, Q = np.linalg.eigh(A)
    c2 = (Q.T @ np.asarray(x0, dtype=float)) ** 2
    target = eps * eps * c2.sum()
    logr = np.log(np.maximum(np.abs(1 - step * lam), 1e-300))

    def err2(k):
        return np.sum(c2 * np.exp(2 * k * logr))

    hi = 1
    while err2(hi) > target:
        hi *= 2
    lo = 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if err2(mid) > target:
            lo = mid
        else:
            hi = mid
    return hi


def rate_bound(eigs, step, eps=1e-6):
    """Iterations guaranteed by the worst contraction factor."""
    rho = float(np.max(np.abs(1 - step * np.asarray(eigs, dtype=float))))
    return math.ceil(math.log(eps) / math.log(rho))


def lab(d=40, seed=0):
    """Ten quadratics: predicted, actual and bound."""
    out = []
    x0 = np.random.default_rng(seed + 1).standard_normal(d)
    for kappa in (10, 30, 100, 300, 1000):
        eigs = np.linspace(1, kappa, d)
        A = quadratic(eigs, seed)
        for name, step in (("inverse_L", 1 / kappa), ("best", 2 / (1 + kappa))):
            out.append({
                "kappa": kappa,
                "step": name,
                "actual": gd_iterations(A, x0, step),
                "predicted": predicted_iterations(A, x0, step),
                "bound": rate_bound(eigs, step),
            })
    return out

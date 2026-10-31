import numpy as np


# provided
def make_data(n=50000, d=10, seed=0):
    rng = np.random.default_rng(seed)
    w = rng.normal(size=d)
    X = rng.normal(size=(n, d))
    y = np.sign(X @ w + 0.5 * rng.normal(size=n))
    return X, y


def _primal(w, X, y, C):
    return 0.5 * w @ w + C * np.sum(np.maximum(0, 1 - y * (X @ w)))


def relative_gap(alpha, X, y, C):
    """(P(w) - D(alpha)) / P(w) with w = X^T (alpha y)."""
    w = X.T @ (alpha * y)
    P = _primal(w, X, y, C)
    D = alpha.sum() - 0.5 * w @ w
    return float((P - D) / P)


def train(X, y, C, tol=1e-4, max_iter=1500, check_every=25):
    """Accelerated projected gradient ascent on the SVM dual."""
    L = np.linalg.eigvalsh(X.T @ X)[-1]
    a = np.zeros(len(y))
    z = a.copy()
    t = 1.0
    gaps = []
    for k in range(1, max_iter + 1):
        g = 1 - y * (X @ (X.T @ (z * y)))
        a_new = np.clip(z + g / L, 0, C)
        t_new = (1 + np.sqrt(1 + 4 * t * t)) / 2
        z = a_new + (t - 1) / t_new * (a_new - a)
        a, t = a_new, t_new
        if k % check_every == 0:
            gaps.append(relative_gap(a, X, y, C))
            if gaps[-1] <= tol:
                break
    return a, X.T @ (a * y), gaps

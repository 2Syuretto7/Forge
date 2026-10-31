import numpy as np

# provided
_rng = np.random.default_rng(4)
# provided
X = _rng.normal(size=(400, 5)) * np.array([1.0, 1.0, 3.0, 0.3, 2.0])
# provided
Y = (X @ np.array([0.5, -1.0, 0.3, 2.0, -0.4]) + _rng.normal(size=400) > 0).astype(float)


def nesterov(grad, x0, alpha, beta, iters):
    """Iterates of Nesterov's method with constant momentum."""
    x = np.array(x0, dtype=float)
    prev = x.copy()
    out = [x.copy()]
    for _ in range(iters):
        y = x + beta * (x - prev)
        prev, x = x, y - alpha * grad(y)
        out.append(x.copy())
    return out


def ridge_logistic(lam):
    """(f, grad) of the ridge-regularized logistic loss on X, Y."""
    def f(w):
        z = X @ w
        sp = np.maximum(z, 0) + np.log1p(np.exp(-np.abs(z)))
        return float(np.mean(sp - Y * z) + 0.5 * lam * w @ w)

    def g(w):
        z = X @ w
        e = np.exp(-np.abs(z))
        s = np.where(z >= 0, 1 / (1 + e), e / (1 + e))
        return X.T @ (s - Y) / len(Y) + lam * w

    return f, g

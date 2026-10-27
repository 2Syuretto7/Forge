import numpy as np


def newton(X, y, l2=1e-3, iters=10):
    n, d = X.shape
    w = np.zeros(d)
    norms = []
    for _ in range(iters):
        s = 0.5 * (1.0 + np.tanh(0.5 * (X @ w)))
        g = X.T @ (s - y) / n + l2 * w
        norms.append(float(np.linalg.norm(g)))
        H = (X * (s * (1 - s))[:, None]).T @ X / n + l2 * np.eye(d)
        w = w - np.linalg.solve(H, g)
    return w, norms

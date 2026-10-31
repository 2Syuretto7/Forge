import numpy as np


def _loss(w, X, y):
    r = X @ w - y
    return float(r @ r / (2 * len(y)))


def sgd(X, y, w0, step, iters, batch, rng):
    """Minibatch SGD on least squares: (final w, losses every 10 steps)."""
    w = np.array(w0, dtype=float)
    losses = []
    for k in range(iters):
        idx = rng.integers(0, len(y), size=batch)
        Xb, yb = X[idx], y[idx]
        w = w - step * Xb.T @ (Xb @ w - yb) / batch
        if k % 10 == 0:
            losses.append(_loss(w, X, y))
    return w, losses


def excess_floor(X, y, step, batch, rng, iters=4000):
    """Average excess loss over the second half of a run started at the optimum."""
    ws = np.linalg.lstsq(X, y, rcond=None)[0]
    f0 = _loss(ws, X, y)
    _, losses = sgd(X, y, ws, step, iters, batch, rng)
    return float(np.mean(losses[len(losses) // 2:]) - f0)

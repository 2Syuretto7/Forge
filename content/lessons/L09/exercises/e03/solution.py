import numpy as np


def gd(grad, x0, lr, steps):
    xs = [np.array(x0, dtype=float)]
    for _ in range(steps):
        xs.append(xs[-1] - lr * grad(xs[-1]))
    return np.array(xs)


def heavy_ball(grad, x0, lr, beta, steps):
    """v <- beta v + grad(x); x <- x - lr v, from v = 0. Return all iterates, shape (steps + 1, d)."""
    x = np.array(x0, dtype=float)
    v = np.zeros_like(x)
    xs = [x.copy()]
    for _ in range(steps):
        v = beta * v + grad(x)
        x = x - lr * v
        xs.append(x.copy())
    return np.array(xs)


def tuned_heavy_ball(A):
    """The optimal (lr, beta) for heavy ball on a quadratic with Hessian A."""
    lam = np.linalg.eigvalsh(A)
    mu, L = lam[0], lam[-1]
    sk = np.sqrt(L / mu)
    return 4.0 / (np.sqrt(L) + np.sqrt(mu)) ** 2, ((sk - 1.0) / (sk + 1.0)) ** 2

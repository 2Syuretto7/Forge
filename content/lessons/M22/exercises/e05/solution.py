import numpy as np


def marginals(joint):
    """(P(X = x_i), P(Y = y_j))."""
    joint = np.asarray(joint, dtype=float)
    return joint.sum(axis=1), joint.sum(axis=0)


def covariance(joint, xs, ys):
    """Cov(X, Y)."""
    px, py = marginals(joint)
    return float(np.asarray(xs) @ np.asarray(joint) @ np.asarray(ys) - (px @ xs) * (py @ ys))


def correlation(joint, xs, ys):
    """Correlation coefficient of X and Y."""
    px, py = marginals(joint)
    xs, ys = np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)
    vx = px @ xs**2 - (px @ xs) ** 2
    vy = py @ ys**2 - (py @ ys) ** 2
    return covariance(joint, xs, ys) / np.sqrt(vx * vy)


def var_of_sum(joint, xs, ys):
    """Var(X + Y) from the joint table."""
    s = np.asarray(xs, dtype=float)[:, None] + np.asarray(ys, dtype=float)[None, :]
    joint = np.asarray(joint, dtype=float)
    m = np.sum(joint * s)
    return float(np.sum(joint * (s - m) ** 2))

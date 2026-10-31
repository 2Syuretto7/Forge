import numpy as np


def kl_optimal(pi_ref, r_hat, beta):
    """pi_ref exp(r_hat / beta), normalized."""
    s = np.log(pi_ref) + np.asarray(r_hat) / beta
    e = np.exp(s - s.max())
    return e / e.sum()


def kl(p, q):
    """KL divergence of p from q."""
    p, q = np.asarray(p), np.asarray(q)
    m = p > 0
    return float(np.sum(p[m] * np.log(p[m] / q[m])))


def true_reward(pi, r):
    """Expected true reward."""
    return float(np.asarray(pi) @ np.asarray(r))


def sweep(pi_ref, r_hat, r, betas):
    """(true reward, KL) of the regularized optimum for each beta."""
    out = []
    for b in betas:
        pi = kl_optimal(pi_ref, r_hat, b)
        out.append((true_reward(pi, r), kl(pi, pi_ref)))
    return out

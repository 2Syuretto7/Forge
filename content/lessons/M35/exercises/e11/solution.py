import math
import numpy as np

N0, D0 = 1e9, 1e10


# provided
def fit_surface(N, D, L, theta0=(2.0, -1.0, 0.3, -1.0, 0.3), iters=200):
    def surface(t):
        u, v = np.log(N / N0), np.log(D / D0)
        return t[0] + np.exp(t[1] - t[2] * u) + np.exp(t[3] - t[4] * v), u, v

    theta = np.array(theta0, dtype=float)
    f, u, v = surface(theta)
    r = L - f
    loss, lam = r @ r, 1e-2
    for _ in range(iters):
        tn, td = np.exp(theta[1] - theta[2] * u), np.exp(theta[3] - theta[4] * v)
        J = np.stack([np.ones_like(u), tn, -u * tn, td, -v * td], axis=1)
        G = J.T @ J
        new = theta + np.linalg.solve(G + lam * np.diag(np.diag(G)), J.T @ r)
        with np.errstate(all="ignore"):
            rn = L - surface(new)[0]
            ln = rn @ rn
        if np.isfinite(ln) and ln < loss:
            theta, r, loss, lam = new, rn, ln, lam / 3
        else:
            lam *= 3
    E, a, alpha, b, beta = theta
    return E, math.exp(a) * N0**alpha, alpha, math.exp(b) * D0**beta, beta


# provided
def optimal_N(chin, C):
    _, A, alpha, B, beta = chin
    return (alpha * A / (beta * B)) ** (1 / (alpha + beta)) * (C / 6) ** (beta / (alpha + beta))


def bootstrap_optimal_N(N, D, L, Cs, B, rng):
    """ln N_opt at each budget for B residual-bootstrap refits."""
    chin = fit_surface(N, D, L)
    E, A, alpha, Bc, beta = chin
    fitted = E + A / N**alpha + Bc / D**beta
    res = L - fitted
    out = np.empty((B, len(Cs)))
    for i in range(B):
        c = fit_surface(N, D, fitted + rng.choice(res, size=len(L), replace=True))
        out[i] = [math.log(optimal_N(c, C)) for C in Cs]
    return out


def log_interval_width(samples, level=0.9):
    """Width of the percentile interval of each column."""
    lo, hi = np.quantile(samples, [(1 - level) / 2, (1 + level) / 2], axis=0)
    return hi - lo

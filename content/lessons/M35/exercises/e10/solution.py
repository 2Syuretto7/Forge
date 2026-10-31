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


def optimal_N(chin, C):
    """Closed-form compute-optimal parameter count."""
    _, A, alpha, B, beta = chin
    G = (alpha * A / (beta * B)) ** (1 / (alpha + beta))
    return G * (C / 6) ** (beta / (alpha + beta))


def optimal_N_numeric(chin, C):
    """Compute-optimal parameter count by search over ln N."""
    E, A, alpha, B, beta = chin

    def loss(lnN):
        N = math.exp(lnN)
        return E + A * N**-alpha + B * (C / (6 * N)) ** -beta

    grid = np.linspace(math.log(1e3), math.log(C / 6) - math.log(1e3), 2001)
    k = int(np.argmin([loss(g) for g in grid]))
    lo, hi = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    phi = (math.sqrt(5) - 1) / 2
    for _ in range(60):
        m1, m2 = hi - phi * (hi - lo), lo + phi * (hi - lo)
        if loss(m1) < loss(m2):
            hi = m2
        else:
            lo = m1
    return math.exp((lo + hi) / 2)


def frontier_exponent(chin):
    """Share of each factor of compute that goes to parameters, in log scale."""
    return chin[4] / (chin[2] + chin[4])

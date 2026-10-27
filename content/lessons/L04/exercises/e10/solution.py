import numpy as np


def gauss(x, mu, s):
    return np.exp(-((x - mu) ** 2) / (2 * s * s)) / (s * np.sqrt(2 * np.pi))


def mixture(x):
    return 0.5 * gauss(x, -2.0, 0.6) + 0.5 * gauss(x, 2.0, 0.6)


def forward_kl_fit(x, p, dx):
    mu = float(np.sum(p * x) * dx)
    s = float(np.sqrt(np.sum(p * (x - mu) ** 2) * dx))
    return mu, s


def reverse_kl(x, p, mu, s, dx):
    q = gauss(x, mu, s)
    m = q > 0
    return float(np.sum(q[m] * np.log(q[m] / p[m])) * dx)


def reverse_kl_fit(x, p, dx, mus, sigmas):
    best = None
    for mu in mus:
        for s in sigmas:
            v = reverse_kl(x, p, mu, s, dx)
            if best is None or v < best[0]:
                best = (v, float(mu), float(s))
    return best[1], best[2]

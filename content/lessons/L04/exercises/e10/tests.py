import numpy as np
import sub

x = np.linspace(-8, 8, 3201)
dx = x[1] - x[0]
p = sub.mixture(x)


def _forward_kl(mu, s):
    q = sub.gauss(x, mu, s)
    return np.sum(p * np.log(p / q)) * dx


def test_target_is_a_density():
    assert abs(np.sum(p) * dx - 1) < 1e-6


def test_forward_fit_covers_both_modes():
    mu, s = sub.forward_kl_fit(x, p, dx)
    assert abs(mu) < 1e-6
    assert abs(s - np.sqrt(4 + 0.36)) < 1e-3
    for dm, ds in [(0.3, 0), (0, 0.3), (0, -0.3)]:
        assert _forward_kl(mu, s) < _forward_kl(mu + dm, s + ds), "moment matching minimizes the forward KL"


def test_reverse_fit_seeks_one_mode():
    mus = np.linspace(-3, 3, 61)
    sigmas = np.linspace(0.2, 3, 57)
    mu, s = sub.reverse_kl_fit(x, p, dx, mus, sigmas)
    assert abs(abs(mu) - 2) < 0.15, mu
    assert abs(s - 0.6) < 0.1, s
    fmu, fs = sub.forward_kl_fit(x, p, dx)
    assert sub.reverse_kl(x, p, mu, s, dx) < sub.reverse_kl(x, p, fmu, fs, dx)

import numpy as np
import sub


def matrix(m, n, s, rng):
    U = np.linalg.qr(rng.standard_normal((m, n)))[0]
    V = np.linalg.qr(rng.standard_normal((n, n)))[0]
    return (U * s) @ V.T


def test_fast_decay():
    rng = np.random.default_rng(0)
    s = 0.8 ** np.arange(150)
    A = matrix(400, 150, s, rng)
    for p in (5, 10):
        errs = [sub.projection_error(A, sub.range_finder(A, 10, p, rng)) for _ in range(10)]
        assert np.mean(errs) <= sub.hmt_factor(10, p) * sub.tail_norm(s, 10)
        assert min(errs) >= sub.tail_norm(s, 10 + p) * (1 - 1e-9)


def test_power_iterations_help_slow_decay():
    rng = np.random.default_rng(1)
    s = 1 / np.sqrt(np.arange(1, 151))
    A = matrix(400, 150, s, rng)
    opt = sub.tail_norm(s, 10)
    plain = sub.projection_error(A, sub.power_range_finder(A, 10, 5, 0, rng))
    powered = sub.projection_error(A, sub.power_range_finder(A, 10, 5, 2, rng))
    assert powered < plain and powered / opt < 1.03, (plain / opt, powered / opt)

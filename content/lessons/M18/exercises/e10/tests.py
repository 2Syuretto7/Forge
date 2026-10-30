import numpy as np
import sub


def test_grad_check_2000():
    x = np.random.default_rng(1).normal(size=2000)
    a, n = sub.grad(x), sub.fd_grad(x)
    assert np.linalg.norm(a - n) / np.linalg.norm(a) < 1e-7


def test_speedup():
    assert sub.speedup(2000) > 100

import numpy as np
import sub


def test_derivation_values():
    assert abs(sub.kl_gauss(2.0, 1.0, 0.0, 1.0) - 2.0) < 1e-12
    assert abs(sub.kl_gauss(0.0, 1.0, 0.0, 2.0) - 0.3181471805599453) < 1e-12
    assert abs(sub.kl_gauss(0.3, 1.7, 0.3, 1.7)) < 1e-15


def test_monte_carlo_agrees():
    for args in [(0.0, 1.0, 1.0, 2.0), (1.0, 0.5, -1.0, 1.5)]:
        exact = sub.kl_gauss(*args)
        mc = sub.kl_gauss_mc(*args, n=200000, seed=1)
        assert abs(mc - exact) < 0.02 * max(1.0, exact), (mc, exact)


def test_grad_mu1_matches_finite_differences():
    for mu1, s1, mu2, s2 in [(0.4, 1.2, -0.3, 0.8), (2.0, 0.5, 1.0, 3.0)]:
        g = sub.grad_kl_mu1(mu1, s1, mu2, s2)
        h = 1e-6
        num = (sub.kl_gauss(mu1 + h, s1, mu2, s2) - sub.kl_gauss(mu1 - h, s1, mu2, s2)) / (2 * h)
        assert abs(g - num) / (abs(g) + abs(num)) < 1e-5

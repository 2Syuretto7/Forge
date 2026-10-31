import numpy as np
import sub


def test_loglik_value_and_edges():
    assert abs(sub.loglik(0.3, 3, 10) - (3 * np.log(0.3) + 7 * np.log(0.7))) < 1e-12
    assert sub.loglik(0.4, 0, 5) == 5 * np.log(0.6)
    assert np.isfinite(sub.loglik(0.999, 10, 10))


def test_grad_matches_finite_differences():
    for p, k, n in [(0.35, 3, 10), (0.8, 17, 20), (0.05, 1, 40)]:
        h = 1e-6
        num = (sub.loglik(p + h, k, n) - sub.loglik(p - h, k, n)) / (2 * h)
        g = sub.dloglik(p, k, n)
        assert abs(g - num) / (abs(g) + abs(num)) < 1e-5


def test_mle_maximizes_and_zeroes_the_gradient():
    k, n = 7, 25
    grid = np.linspace(0.001, 0.999, 999)
    best = grid[np.argmax([sub.loglik(p, k, n) for p in grid])]
    assert abs(sub.mle(k, n) - best) < 0.002
    assert abs(sub.dloglik(sub.mle(k, n), k, n)) < 1e-9


def test_standard_error():
    assert abs(sub.standard_error(50, 100) - 0.05) < 1e-12
    assert sub.standard_error(0, 10) == 0.0

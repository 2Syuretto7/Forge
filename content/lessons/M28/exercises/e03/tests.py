import numpy as np
import sub

rng = np.random.default_rng(3)


def test_signs():
    for _ in range(30):
        x = rng.normal(size=8)
        w = rng.dirichlet(np.ones(8))
        assert sub.jensen_gap(np.exp, x, w) >= -1e-12
        assert sub.jensen_gap(np.square, x, w) >= -1e-12
        assert sub.jensen_gap(np.log, np.exp(x), w) <= 1e-12


def test_variance_and_am_gm():
    x = rng.normal(size=1000)
    assert abs(sub.jensen_gap(np.square, x) - x.var()) < 1e-12
    a, g = sub.am_gm([1.0, 9.0])
    assert a == 5.0 and abs(g - 3.0) < 1e-12
    for _ in range(20):
        a, g = sub.am_gm(rng.uniform(0.1, 10, size=5))
        assert g <= a + 1e-12


def test_log_mean_exp():
    x = rng.normal(size=50) * 300
    assert sub.log_mean_exp(x) >= x.mean()
    assert abs(sub.log_mean_exp([0.0, 0.0]) - 0.0) < 1e-15
    assert abs(sub.log_mean_exp([1000.0, 1000.0]) - 1000.0) < 1e-12

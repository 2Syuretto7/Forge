import numpy as np
import sub


def test_correlated_sum_by_simulation():
    C = sub.equicorrelated(100, 0.1, 2.0)
    assert C.shape == (100, 100) and abs(C[0, 0] - 4) < 1e-12 and abs(C[0, 1] - 0.4) < 1e-12
    L = np.linalg.cholesky(C)
    x = np.random.default_rng(14).standard_normal((20000, 100)) @ L.T
    observed = x.sum(axis=1).var()
    assert abs(observed / sub.var_sum(C) - 1) < 0.05
    assert abs(sub.var_sum(C) / sub.var_sum_independent(C) - 10.9) < 1e-9


def test_effective_n():
    assert abs(sub.effective_n(100, 0.1) - 100 / 10.9) < 1e-12
    assert sub.effective_n(100, 0.0) == 100
    assert abs(sub.effective_n(1000, 0.1) - 1000 / 100.9) < 1e-12


def test_negative_correlation_cancels():
    C = sub.equicorrelated(5, -0.25)
    assert abs(sub.var_sum(C)) < 1e-12 and sub.var_sum_independent(C) == 5

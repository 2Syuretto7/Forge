import math
import numpy as np
import sub


def test_sgd_noise_floor():
    rng = np.random.default_rng(0)
    for eta in (0.3, 0.15):
        x = sub.sgd_chains(2.0, 1.0, eta, 300, 20000, rng)
        assert abs(x.var() / sub.sgd_stationary_var(2.0, 1.0, eta) - 1) < 0.05
    ratio = sub.sgd_stationary_var(2.0, 1.0, 0.01) / sub.sgd_stationary_var(2.0, 1.0, 0.02)
    assert abs(ratio - 0.5) < 0.01
    assert sub.sgd_stationary_var(2.0, 1.0, 1.0) == math.inf


def test_ula_bias():
    rng = np.random.default_rng(1)
    for h in (0.4, 0.1):
        x = sub.ula_chains(lambda x: -x, np.zeros(20000), h, 300, rng)
        v = sub.ula_stationary_var(1.0, h)
        assert abs(x.var() / v - 1) < 0.05
        assert v > 1.0
    assert sub.ula_stationary_var(1.0, 0.1) < sub.ula_stationary_var(1.0, 0.4)

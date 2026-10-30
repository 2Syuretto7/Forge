import numpy as np
import sub

rng = np.random.default_rng(12)
true_z = rng.normal(0, 2.0, 50_000)
y = (rng.random(50_000) < 1 / (1 + np.exp(-true_z))).astype(int)
z = 2.5 * true_z


def test_grad_derivative():
    for T in (0.7, 1.5, 3.0):
        num = (sub.nll(z, y, T + 1e-6) - sub.nll(z, y, T - 1e-6)) / 2e-6
        assert abs(num - sub.dnll_dT(z, y, T)) < 1e-6


def test_recovers_temperature():
    T = sub.fit_temperature(z, y)
    assert abs(T - 2.5) < 0.1
    assert sub.nll(z, y, T) < sub.nll(z, y, 1.0)

import numpy as np
import sub

rng = np.random.default_rng(3)
x = np.logspace(1, 4, 9)
y = 7.0 * x ** -0.3 * np.exp(0.05 * rng.standard_normal(9))


def test_grad_log_mse():
    theta = np.array([1.3, 0.2])
    _, g = sub.log_mse(theta, x, y)
    num = []
    for i in range(2):
        e = np.zeros(2)
        e[i] = 1e-6
        num.append((sub.log_mse(theta + e, x, y)[0] - sub.log_mse(theta - e, x, y)[0]) / 2e-6)
    assert np.allclose(g, num, atol=1e-8)


def test_fit_recovers_exact_data():
    k, a = sub.fit_power_law(x, 7.0 * x ** -0.3)
    assert abs(k - 7.0) < 1e-9 and abs(a - 0.3) < 1e-12


def test_fit_is_the_minimum():
    k, a = sub.fit_power_law(x, y)
    _, g = sub.log_mse(np.array([np.log(k), a]), x, y)
    assert np.allclose(g, 0, atol=1e-10)

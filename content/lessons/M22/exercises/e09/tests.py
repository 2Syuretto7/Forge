import numpy as np
import sub

V = np.array([0.0, 1.0, 2.0, 10.0, 50.0])
P = np.array([0.3, 0.3, 0.2, 0.15, 0.05])


def test_grad_dmse():
    h = 1e-6
    for c in (-3.0, 0.5, 4.2, 20.0):
        num = (sub.mse(c + h, V, P) - sub.mse(c - h, V, P)) / (2 * h)
        assert abs(num - sub.dmse_dc(c, V, P)) < 1e-6 * max(1, abs(num))


def test_decomposition():
    m = sub.best_constant(V, P)
    var = float(np.sum(P * (V - m) ** 2))
    assert abs(sub.dmse_dc(m, V, P)) < 1e-12
    for c in (-1.0, 0.0, 3.0, 7.5):
        assert abs(sub.mse(c, V, P) - (var + (m - c) ** 2)) < 1e-9


def test_mean_and_median_differ_on_skewed_data():
    m = sub.best_constant(V, P)
    med = sub.best_constant_abs(V, P)
    assert abs(m - 4.7) < 1e-12 and med == 1.0
    grid = np.linspace(-5, 60, 1301)
    assert sub.mae(med, V, P) <= min(sub.mae(c, V, P) for c in grid) + 1e-12
    assert sub.mse(m, V, P) <= min(sub.mse(c, V, P) for c in grid) + 1e-12

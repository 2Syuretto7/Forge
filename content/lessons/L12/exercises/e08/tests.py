import numpy as np
import sub

c = np.array([3.0, 1.0, 0.5, 2.0])


def test_epochs_and_temperature():
    assert np.allclose(sub.domain_epochs([0.5, 0.5], [100, 10], 100), [0.5, 5])
    w = sub.temperature_weights([1000, 10], 1)
    assert np.allclose(w, [1000 / 1010, 10 / 1010])
    flat = sub.temperature_weights([1000, 10], 100)
    assert flat[1] > w[1] and abs(flat.sum() - 1) < 1e-12


def test_grad_mixture_objective():
    z = np.array([0.2, -0.4, 0.1, 0.3])
    _, g = sub.mixture_objective(z, c, 0.3, 1e6)
    for i in range(4):
        e = np.zeros(4)
        e[i] = 1e-6
        num = (sub.mixture_objective(z + e, c, 0.3, 1e6)[0] - sub.mixture_objective(z - e, c, 0.3, 1e6)[0]) / 2e-6
        assert abs(g[i] - num) < 1e-8


def test_gradient_descent_finds_the_closed_form():
    z = np.zeros(4)
    for _ in range(1000):
        _, g = sub.mixture_objective(z, c, 0.3, 1e6)
        z -= 50.0 * g
    p = np.exp(z - z.max())
    p /= p.sum()
    assert np.allclose(p, sub.optimal_mixture(c, 0.3), atol=1e-6)

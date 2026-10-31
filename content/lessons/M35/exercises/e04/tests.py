import numpy as np
import sub

X = np.logspace(0, 2, 30)


def test_grad_jacobian():
    th = np.array([1.2, 2.5, 0.7])
    J = sub.jacobian(th, X)
    h = 1e-6
    for j in range(3):
        e = np.zeros(3)
        e[j] = h
        num = (sub.model(th + e, X) - sub.model(th - e, X)) / (2 * h)
        assert np.max(np.abs(num - J[:, j])) < 1e-7


def test_recovers():
    rng = np.random.default_rng(0)
    y = sub.model([1.7, 2.0, 0.5], X) + 0.003 * rng.standard_normal(30)
    th = sub.gauss_newton(X, y, [1.5, 1.5, 0.4])
    assert np.max(np.abs(th - [1.7, 2.0, 0.5])) < 0.05

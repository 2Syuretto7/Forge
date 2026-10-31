import numpy as np
import sub


def test_grad_logistic():
    X, y = sub.make_task(100, 4, 1)
    w = np.array([0.3, -0.2, 0.5, 0.1])
    h = 1e-6
    num = np.array([(sub.loss(w + h * e, X, y) - sub.loss(w - h * e, X, y)) / (2 * h) for e in np.eye(4)])
    assert np.allclose(num, sub.grad(w, X, y), atol=1e-8)


def test_gap_scaling():
    g = lambda n, d: np.mean([sub.gap(n, d, s) for s in range(4)])
    assert g(100, 5) > 2 * g(800, 5) > 0
    assert g(200, 20) > g(200, 5)

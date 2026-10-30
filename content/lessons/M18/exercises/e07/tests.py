import numpy as np
import sub

Q = np.diag([4.0, 1.0])
f = lambda x: 0.5 * x @ Q @ x  # noqa: E731
grad = lambda x: Q @ x  # noqa: E731


def test_grad_bound_tight_along_top_eigenvector():
    x = np.array([1.0, 0.0])
    g = grad(x)
    for eta in (0.05, 0.25, 0.4):
        assert abs(sub.gd_step_decrease(f, grad, x, eta) - sub.descent_bound(g @ g, 4.0, eta)) < 1e-12


def test_grad_bound_holds_elsewhere():
    x = np.array([0.3, 1.0])
    g = grad(x)
    for eta in (0.05, 0.25, 0.45):
        assert sub.gd_step_decrease(f, grad, x, eta) >= sub.descent_bound(g @ g, 4.0, eta) - 1e-12
    assert sub.gd_step_decrease(f, grad, np.array([1.0, 0.0]), 0.6) < 0


def test_taylor_third_order():
    fn = lambda v: np.exp(v[0]) * np.sin(v[1])  # noqa: E731
    x = np.array([0.2, 0.7])
    e, s, c = np.exp(0.2), np.sin(0.7), np.cos(0.7)
    g = np.array([e * s, e * c])
    H = np.array([[e * s, e * c], [e * c, -e * s]])
    d = np.array([0.6, -0.8])
    e1 = abs(fn(x + 0.02 * d) - sub.taylor2(fn(x), g, H, 0.02 * d))
    e2 = abs(fn(x + 0.01 * d) - sub.taylor2(fn(x), g, H, 0.01 * d))
    assert 7 < e1 / e2 < 9

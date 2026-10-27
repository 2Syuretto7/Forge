import numpy as np
import sub

Q = np.diag([4.0, 1.0])


def f(x):
    return 0.5 * x @ Q @ x


def grad(x):
    return Q @ x


def test_bound_is_tight_along_the_top_eigenvector():
    x = np.array([1.0, 0.0])
    g = grad(x)
    for eta in [0.05, 0.25, 0.4]:
        assert abs(sub.gd_step_decrease(f, grad, x, eta) - sub.descent_bound(g @ g, 4.0, eta)) < 1e-12


def test_bound_holds_in_other_directions():
    x = np.array([0.3, 1.0])
    g = grad(x)
    for eta in [0.05, 0.25, 0.45]:
        assert sub.gd_step_decrease(f, grad, x, eta) >= sub.descent_bound(g @ g, 4.0, eta) - 1e-12


def test_too_large_a_step_increases_f():
    x = np.array([1.0, 0.0])
    assert sub.gd_step_decrease(f, grad, x, 0.6) < 0, "eta above 2/L must increase f"


def test_taylor_error_is_third_order():
    fn = lambda v: np.exp(v[0]) * np.sin(v[1])  # noqa: E731
    x = np.array([0.2, 0.7])
    g = np.array([np.exp(0.2) * np.sin(0.7), np.exp(0.2) * np.cos(0.7)])
    H = np.array([[np.exp(0.2) * np.sin(0.7), np.exp(0.2) * np.cos(0.7)],
                  [np.exp(0.2) * np.cos(0.7), -np.exp(0.2) * np.sin(0.7)]])
    d = np.array([0.6, -0.8])
    e1 = abs(fn(x + 0.02 * d) - sub.taylor2(fn(x), g, H, 0.02 * d))
    e2 = abs(fn(x + 0.01 * d) - sub.taylor2(fn(x), g, H, 0.01 * d))
    assert 7 < e1 / e2 < 9, f"ratio {e1 / e2:.2f}"

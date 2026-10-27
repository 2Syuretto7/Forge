import numpy as np
import sub

rng = np.random.default_rng(3)
A = rng.normal(size=(4, 4))
S = A + A.T


def f(x):
    return float(0.5 * x.ravel() @ S @ x.ravel() + np.sum(np.sin(x)))


def grad_f(x):
    return (S @ x.ravel()).reshape(x.shape) + np.cos(x)


def test_numerical_gradient_of_a_matrix_input():
    x = rng.normal(size=(2, 2))
    g = sub.numerical_gradient(f, x)
    assert g.shape == (2, 2)
    assert np.allclose(g, grad_f(x), atol=1e-8)


def test_input_is_not_modified():
    x = rng.normal(size=4)
    x0 = x.copy()
    sub.numerical_gradient(f, x)
    assert np.array_equal(x, x0)


def test_grad_check_accepts_correct_gradient():
    ok, err = sub.check_gradient(f, grad_f, rng.normal(size=4))
    assert ok and err < 1e-8


def test_grad_check_detects_wrong_gradient():
    wrong = lambda x: grad_f(x) + 1e-3 * np.cos(x)  # noqa: E731
    ok, err = sub.check_gradient(f, wrong, rng.normal(size=4))
    assert not ok, f"a 0.1% error in the gradient must fail the check (err={err:.2e})"


def test_relative_error_is_scale_free():
    a = rng.normal(size=5)
    assert abs(sub.relative_error(a, 1.01 * a) - sub.relative_error(1e6 * a, 1.01e6 * a)) < 1e-12
    assert sub.relative_error(np.zeros(3), np.zeros(3)) == 0.0

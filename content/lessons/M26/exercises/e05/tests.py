import numpy as np
import sub


def f(x):
    return np.exp(np.sin(x)) / np.sqrt(x)


def df(x):
    return np.exp(np.sin(x)) * (np.cos(x) / np.sqrt(x) - 0.5 * x**-1.5)


X = 1.3


def test_grad_complex_step_is_exact():
    assert abs(sub.complex_step(f, X) - df(X)) < 1e-15 * abs(df(X))
    assert abs(sub.complex_step(np.sin, 0.5, 1e-200) - np.cos(0.5)) < 1e-16


def test_grad_finite_differences():
    assert abs(sub.forward_diff(f, X, 1e-8) - df(X)) < 1e-6
    assert abs(sub.central_diff(f, X, 1e-5) - df(X)) < 1e-9


def test_v_shape():
    hs = [1e-2, 1e-5, 1e-8, 1e-11, 1e-14]
    e = sub.error_curve(f, df, X, hs, sub.forward_diff)
    assert e[2] < e[0] and e[2] < e[4] and e[4] > 1e-3
    c = sub.error_curve(f, df, X, [1e-5, 1e-10, 1e-20, 1e-100], sub.complex_step)
    assert max(c[1:]) < 1e-14

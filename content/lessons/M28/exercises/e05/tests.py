import numpy as np
import sub


def test_quadratic():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    assert sub.smooth_strong(A) == (3.0, 1.0) or np.allclose(sub.smooth_strong(A), (3.0, 1.0))
    assert abs(sub.condition_number(A) - 3) < 1e-12
    ax = sub.level_set_axes(A)
    assert np.allclose(ax, [np.sqrt(2), np.sqrt(2 / 3)])
    assert abs((ax[0] / ax[-1]) ** 2 - sub.condition_number(A)) < 1e-12


def test_narrow_valley():
    wide = np.diag([1.0, 10.0])
    narrow = np.diag([1.0, 1000.0])
    r_wide = sub.level_set_axes(wide)
    r_narrow = sub.level_set_axes(narrow)
    assert abs(r_wide[1] / r_narrow[1] - 10) < 1e-9
    assert abs(sub.condition_number(narrow) / sub.condition_number(wide) - 100) < 1e-9


def test_logistic_bound():
    rng = np.random.default_rng(5)
    X = rng.normal(size=(300, 4))
    L = sub.logistic_smoothness(X)
    w = rng.normal(size=4)
    z = X @ w
    s = 1 / (1 + np.exp(-z))
    H = X.T @ (X * (s * (1 - s))[:, None]) / 300
    assert np.linalg.eigvalsh(H)[-1] <= L + 1e-12

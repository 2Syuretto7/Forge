import warnings
import numpy as np
import sub

rng = np.random.default_rng(4)
X = rng.normal(size=(60, 3))
y = (X @ np.array([1.0, -1.0, 0.5]) + 0.3 * rng.normal(size=60) > 0).astype(float)


def test_sigmoid_is_stable():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s = sub.sigmoid(np.array([-1000.0, 0.0, 1000.0]))
    assert np.allclose(s, [0.0, 0.5, 1.0])


def test_loss_matches_naive_formula():
    w, b = rng.normal(size=3), 0.2
    s = 1 / (1 + np.exp(-(X @ w + b)))
    naive = -np.mean(y * np.log(s) + (1 - y) * np.log(1 - s))
    assert abs(sub.logistic_loss(w, b, X, y) - naive) < 1e-12


def test_grad_matches_finite_differences():
    w, b = rng.normal(size=3), -0.4
    dw, db = sub.logistic_grad(w, b, X, y)
    g = np.append(dw, db)
    num = np.zeros(4)
    for j in range(4):
        e = np.zeros(4)
        e[j] = 1e-6
        f = lambda v: sub.logistic_loss(v[:3], v[3], X, y)  # noqa: E731
        num[j] = (f(np.append(w, b) + e) - f(np.append(w, b) - e)) / 2e-6
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5

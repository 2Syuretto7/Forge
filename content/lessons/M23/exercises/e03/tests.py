import math
import numpy as np
import sub

rng = np.random.default_rng(3)
A = rng.normal(size=(3, 3))
S = A @ A.T + 0.5 * np.eye(3)
MU = np.array([1.0, -1.0, 2.0])


def test_grad_score():
    X = rng.normal(size=(6, 3)) + MU
    h = 1e-6
    g = sub.score(X, MU, S)
    for k in range(3):
        e = np.zeros(3)
        e[k] = h
        num = (sub.logpdf(X + e, MU, S) - sub.logpdf(X - e, MU, S)) / (2 * h)
        assert np.allclose(num, g[:, k], rtol=1e-5, atol=1e-7)


def test_one_dimension_and_diagonal():
    x = np.array([[0.3], [2.0]])
    expected = -0.5 * ((x[:, 0] - 1) / 2) ** 2 - math.log(2 * math.sqrt(2 * math.pi))
    assert np.allclose(sub.logpdf(x, np.array([1.0]), np.array([[4.0]])), expected)
    D = np.diag([1.0, 4.0, 0.25])
    X = rng.normal(size=(5, 3))
    one = sum(-0.5 * X[:, i] ** 2 / D[i, i] - 0.5 * math.log(2 * math.pi * D[i, i]) for i in range(3))
    assert np.allclose(sub.logpdf(X, np.zeros(3), D), one)


def test_high_dimension_is_finite():
    d = 256
    lp = sub.logpdf(np.zeros((1, d)), np.zeros(d), 0.01 * np.eye(d))
    assert np.isfinite(lp).all() and abs(lp[0] - (-128 * math.log(2 * math.pi * 0.01))) < 1e-8

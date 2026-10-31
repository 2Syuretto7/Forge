import numpy as np
import sub

S = np.array([[4.0, 1.5, 0.0], [1.5, 2.0, -0.6], [0.0, -0.6, 1.0]])
MU = np.array([2.0, 0.0, -1.0])


def test_sample_moments():
    X = sub.sample(MU, S, 200000, np.random.default_rng(5))
    assert X.shape == (200000, 3)
    assert np.allclose(X.mean(axis=0), MU, atol=0.02) and np.allclose(np.cov(X, rowvar=False), S, atol=0.04)


def test_whitenings():
    X = sub.sample(MU, S, 2000, np.random.default_rng(6))
    for W in (sub.whiten(X), sub.zca(X)):
        assert np.allclose(W.mean(axis=0), 0, atol=1e-12)
        assert np.allclose(np.cov(W, rowvar=False), np.eye(3), atol=1e-10)


def test_zca_stays_closest():
    X = sub.sample(MU, S, 2000, np.random.default_rng(7))
    Xc = X - X.mean(axis=0)
    d_zca = np.sum((sub.zca(X) - Xc) ** 2)
    d_chol = np.sum((sub.whiten(X) - Xc) ** 2)
    assert d_zca < d_chol
    rng = np.random.default_rng(8)
    for _ in range(5):
        Q = np.linalg.qr(rng.normal(size=(3, 3)))[0]
        assert d_zca <= np.sum((sub.zca(X) @ Q - Xc) ** 2) + 1e-9

import math
import numpy as np
import sub

rng = np.random.default_rng(20)
A = rng.normal(size=(4, 4))
S = A @ A.T + 0.5 * np.eye(4)
MU = np.array([1.0, 0.0, -2.0, 0.5])


def test_sample_and_logpdf():
    X = sub.sample(MU, S, 100000, np.random.default_rng(21))
    assert np.allclose(X.mean(axis=0), MU, atol=0.05) and np.allclose(np.cov(X, rowvar=False), S, atol=0.1 * np.abs(S).max())
    Y = X[:5]
    D = Y - MU
    direct = -0.5 * np.sum(D @ np.linalg.inv(S) * D, axis=1) - 0.5 * math.log((2 * math.pi) ** 4 * np.linalg.det(S))
    assert np.allclose(sub.logpdf(Y, MU, S), direct)
    assert np.isfinite(sub.logpdf(np.zeros((2, 256)), np.zeros(256), 1e-3 * np.eye(256))).all()


def test_condition():
    m, V = sub.condition(MU, S, [0, 2], [2.0, -1.0])
    P = np.linalg.inv(S)
    # The conditional covariance is the inverse of the precision matrix's unobserved block.
    assert np.allclose(V, np.linalg.inv(P[np.ix_([1, 3], [1, 3])]))
    x = np.array([2.0, 0.0, -1.0, 0.0])
    x[[1, 3]] = m
    assert np.allclose((P @ (x - MU))[[1, 3]], 0, atol=1e-10)


def test_tracker_halves_the_error():
    x, z = sub.simulate_target(2000, seed=7)
    f = sub.track(z)
    raw = math.sqrt(np.mean((z - x) ** 2))
    filt = math.sqrt(np.mean((f - x)[50:] ** 2))
    assert f.shape == (2000,)
    assert filt < 0.5 * raw, (filt, raw)

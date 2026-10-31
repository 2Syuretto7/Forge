import numpy as np
import sub

rng = np.random.default_rng(2)
X = rng.normal(size=(500, 4)) @ rng.normal(size=(4, 4)) + np.array([1.0, -2.0, 0.5, 3.0])


def test_against_numpy():
    m, S = sub.mean_and_cov(X)
    assert np.allclose(m, X.mean(axis=0)) and np.allclose(S, np.cov(X, rowvar=False))
    assert np.allclose(np.diag(sub.correlation_matrix(S)), 1)
    assert np.allclose(sub.correlation_matrix(S), np.corrcoef(X, rowvar=False))


def test_combinations_and_psd():
    m, S = sub.mean_and_cov(X)
    for _ in range(10):
        a = rng.normal(size=4)
        assert abs(sub.var_of_combination(S, a) - np.var(X @ a, ddof=1)) < 1e-9 * max(1, np.var(X @ a))
    assert np.linalg.eigvalsh(S).min() > -1e-12
    assert abs(sub.var_of_combination(np.array([[4.0, 2.0], [2.0, 3.0]]), [1, -1]) - 3) < 1e-12


def test_affine():
    m, S = sub.mean_and_cov(X)
    A = rng.normal(size=(2, 4))
    b = np.array([5.0, -1.0])
    m2, S2 = sub.affine_moments(m, S, A, b)
    m3, S3 = sub.mean_and_cov(X @ A.T + b)
    assert np.allclose(m2, m3) and np.allclose(S2, S3)

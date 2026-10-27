import numpy as np
import sub

rng = np.random.default_rng(4)
A = rng.normal(size=(9, 5))


def test_factorization_reconstructs_A():
    Q, R = sub.qr(A)
    assert Q.shape == (9, 5) and R.shape == (5, 5)
    assert np.allclose(Q @ R, A, atol=1e-12)


def test_structure():
    Q, R = sub.qr(A)
    assert np.allclose(np.tril(R, -1), 0), "R must be upper triangular"
    assert np.all(np.diag(R) > 0), "diagonal of R must be positive"
    assert np.allclose(Q.T @ Q, np.eye(5), atol=1e-12)


def test_matches_numpy_up_to_signs():
    Q, R = sub.qr(A)
    Qn, Rn = np.linalg.qr(A)
    s = np.sign(np.diag(Rn))
    assert np.allclose(R, s[:, None] * Rn, atol=1e-10)


def test_back_substitution():
    R = np.triu(rng.normal(size=(6, 6))) + 4 * np.eye(6)
    y = rng.normal(size=6)
    x = sub.back_substitute(R, y)
    assert np.allclose(R @ x, y, atol=1e-12)


def test_least_squares_via_qr():
    b = rng.normal(size=9)
    Q, R = sub.qr(A)
    x = sub.back_substitute(R, Q.T @ b)
    ref, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.allclose(x, ref, atol=1e-10)

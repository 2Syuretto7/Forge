import numpy as np
import sub

rng = np.random.default_rng(4)
A = rng.normal(size=(9, 5))


def test_factorization():
    Q, R = sub.qr(A)
    assert Q.shape == (9, 5) and R.shape == (5, 5)
    assert np.allclose(Q @ R, A, atol=1e-12)
    assert np.allclose(np.tril(R, -1), 0) and np.all(np.diag(R) > 0)
    Qn, Rn = np.linalg.qr(A)
    assert np.allclose(R, np.sign(np.diag(Rn))[:, None] * Rn, atol=1e-10)


def test_back_substitution():
    R = np.triu(rng.normal(size=(6, 6))) + 4 * np.eye(6)
    y = rng.normal(size=6)
    assert np.allclose(R @ sub.back_substitute(R, y), y, atol=1e-12)


def test_least_squares():
    b = rng.normal(size=9)
    ref, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.allclose(sub.lstsq_qr(A, b), ref, atol=1e-10)

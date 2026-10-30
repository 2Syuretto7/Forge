import numpy as np
import sub

rng = np.random.default_rng(3)
Q, _ = np.linalg.qr(rng.normal(size=(5, 5)))
EIG = [1.0, 2.0, 5.0, 7.0, 10.0]
A = Q @ np.diag(EIG) @ Q.T


def test_nearest():
    lam, v = sub.inverse_iteration(A, 4.6)
    assert abs(lam - 5.0) < 1e-10
    assert np.linalg.norm(A @ v - 5 * v) < 1e-8


def test_all():
    assert sub.all_by_shifts(A, [0.9, 2.2, 4.8, 6.6, 9.5, 10.4]) == EIG

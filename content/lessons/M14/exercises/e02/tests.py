import numpy as np
import sub

rng = np.random.default_rng(2)
U0, _ = np.linalg.qr(rng.normal(size=(30, 6)))
V0, _ = np.linalg.qr(rng.normal(size=(12, 6)))
S0 = np.array([10.0, 6.0, 3.0, 1.5, 0.7, 0.3])
A = U0 @ np.diag(S0) @ V0.T


def test_top():
    s, u, v = sub.top_singular(A)
    assert abs(s - 10) < 1e-10
    assert abs(abs(u @ U0[:, 0]) - 1) < 1e-10 and abs(abs(v @ V0[:, 0]) - 1) < 1e-10


def test_deflation():
    U, s, Vt = sub.svd_deflation(A, 4)
    assert U.shape == (30, 4) and Vt.shape == (4, 12)
    assert np.allclose(s, S0[:4], atol=1e-8)
    assert np.allclose(np.abs(np.sum(U * U0[:, :4], axis=0)), 1, atol=1e-8)

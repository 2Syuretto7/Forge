import numpy as np
import sub


def test_matches_full_svd():
    rng = np.random.default_rng(0)
    A = rng.standard_normal((500, 15)) @ rng.standard_normal((15, 200)) + 1e-6 * rng.standard_normal((500, 200))
    U, s, Vt = sub.rsvd(A, 15, rng=rng)
    assert U.shape == (500, 15) and s.shape == (15,) and Vt.shape == (15, 200)
    full = np.linalg.svd(A, compute_uv=False)
    assert np.max(np.abs(s - full[:15]) / full[:15]) < 1e-6
    assert np.linalg.norm(A - (U * s) @ Vt) < 2 * np.sqrt(np.sum(full[15:] ** 2))
    assert np.allclose(U.T @ U, np.eye(15), atol=1e-10)


def test_grad_top_singular_value():
    rng = np.random.default_rng(1)
    A = rng.standard_normal((6, 4))
    G = sub.grad_top_singular_value(A)
    h = 1e-6
    for i, j in ((0, 0), (2, 3), (5, 1), (4, 2)):
        E = np.zeros_like(A)
        E[i, j] = h
        num = (sub.top_singular_value(A + E) - sub.top_singular_value(A - E)) / (2 * h)
        assert abs(num - G[i, j]) < 1e-7

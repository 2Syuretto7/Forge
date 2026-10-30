import numpy as np
import sub

rng = np.random.default_rng(2)


def test_plane_in_3d():
    A = np.array([[1.0, 0], [0, 1], [0, 0]])
    N = sub.complement_basis(A)
    assert N.shape == (3, 1) and np.allclose(np.abs(N[:, 0]), [0, 0, 1])
    p, r = sub.split(np.array([1.0, 2, 3]), A)
    assert np.allclose(p, [1, 2, 0]) and np.allclose(r, [0, 0, 3])


def test_invariant_complement():
    for _ in range(50):
        m = int(rng.integers(2, 9))
        n = int(rng.integers(1, m))
        A, b = rng.normal(size=(m, n)), rng.normal(size=m)
        N = sub.complement_basis(A)
        assert N.shape == (m, m - n)
        assert np.allclose(A.T @ N, 0, atol=1e-10)
        assert np.allclose(N.T @ N, np.eye(m - n), atol=1e-10)
        p, r = sub.split(b, A)
        assert np.allclose(p + r, b)
        assert np.allclose(A.T @ r, 0, atol=1e-9)
        assert np.allclose(N @ (N.T @ r), r, atol=1e-9)

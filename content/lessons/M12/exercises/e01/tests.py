import numpy as np
import sub

rng = np.random.default_rng(1)


def test_line():
    p = sub.project_onto_line(np.array([1.0, 0.0]), np.array([3.0, 4.0]))
    assert np.allclose(p, [0.36, 0.48])


def test_matches_lstsq_and_keeps_subspace():
    A, b = rng.normal(size=(8, 3)), rng.normal(size=8)
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.allclose(sub.project(b, A), A @ x)
    v = A @ rng.normal(size=3)
    assert np.allclose(sub.project(v, A), v)


def test_invariant_projection_properties():
    for _ in range(50):
        m = int(rng.integers(2, 10))
        n = int(rng.integers(1, m + 1))
        A, b = rng.normal(size=(m, n)), rng.normal(size=m)
        P = sub.projection_matrix(A)
        assert np.allclose(P, P.T, atol=1e-9)
        assert np.allclose(P @ P, P, atol=1e-9)
        assert np.allclose(A.T @ (b - sub.project(b, A)), 0, atol=1e-9)

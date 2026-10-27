import numpy as np
import sub

rng = np.random.default_rng(9)


def test_reconstruction_tall():
    A = rng.normal(size=(8, 4))
    U, s, Vt = sub.svd_via_eig(A)
    assert U.shape == (8, 4) and s.shape == (4,) and Vt.shape == (4, 4)
    assert np.allclose(U @ np.diag(s) @ Vt, A, atol=1e-10)


def test_singular_values_match_numpy():
    A = rng.normal(size=(6, 5))
    _, s, _ = sub.svd_via_eig(A)
    assert np.allclose(s, np.linalg.svd(A, compute_uv=False), atol=1e-10)
    assert np.all(np.diff(s) <= 0), "singular values must be descending"


def test_orthonormal_factors():
    A = rng.normal(size=(7, 3))
    U, s, Vt = sub.svd_via_eig(A)
    assert np.allclose(U.T @ U, np.eye(3), atol=1e-10)
    assert np.allclose(Vt @ Vt.T, np.eye(3), atol=1e-10)


def test_wide_and_rank_deficient():
    B = rng.normal(size=(3, 2)) @ rng.normal(size=(2, 6))  # rank 2, shape (3, 6)
    U, s, Vt = sub.svd_via_eig(B)
    assert s.shape == (2,), f"expected numerical rank 2, got {s.shape[0]}"
    assert np.allclose(U @ np.diag(s) @ Vt, B, atol=1e-9)

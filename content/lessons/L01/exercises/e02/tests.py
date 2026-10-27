import numpy as np
import sub

rng = np.random.default_rng(1)
A = rng.normal(size=(8, 3))
b = rng.normal(size=8)


def test_line_projection_formula():
    a = np.array([3.0, 4.0])
    p = sub.project_onto_line(np.array([1.0, 0.0]), a)
    assert np.allclose(p, [0.36, 0.48]), f"got {p}"


def test_shapes():
    assert sub.projection_matrix(A).shape == (8, 8)
    assert sub.project(b, A).shape == (8,)


def test_projection_is_symmetric_and_idempotent():
    P = sub.projection_matrix(A)
    assert np.allclose(P, P.T, atol=1e-10), "P should equal its transpose"
    assert np.allclose(P @ P, P, atol=1e-10), "projecting twice should change nothing"


def test_residual_orthogonal_to_columns():
    r = b - sub.project(b, A)
    assert np.allclose(A.T @ r, 0, atol=1e-10), f"A^T r = {A.T @ r}"


def test_matches_least_squares_fit():
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.allclose(sub.project(b, A), A @ x, atol=1e-10)


def test_vectors_in_the_subspace_are_unchanged():
    v = A @ rng.normal(size=3)
    assert np.allclose(sub.project(v, A), v, atol=1e-10)

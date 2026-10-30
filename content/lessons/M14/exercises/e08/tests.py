import numpy as np
import sub

rng = np.random.default_rng(8)
A = rng.normal(size=(8, 3))
b = rng.normal(size=8)


def test_agrees_with_normal_equations():
    p = A @ np.linalg.solve(A.T @ A, A.T @ b)
    assert np.allclose(sub.project_svd(b, A), p)
    assert sub.column_space_basis(A).shape == (8, 3)


def test_dependent_columns():
    B = np.column_stack([A, A[:, 0] - 2 * A[:, 2]])
    assert sub.column_space_basis(B).shape == (8, 3)
    assert np.allclose(sub.project_svd(b, B), sub.project_svd(b, A))
    v = B @ rng.normal(size=4)
    assert np.allclose(sub.project_svd(v, B), v)

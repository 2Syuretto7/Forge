import numpy as np
import sub

rng = np.random.default_rng(3)


def test_orthonormal_columns():
    A = rng.normal(size=(10, 4))
    Q = sub.gram_schmidt(A)
    assert Q.shape == (10, 4)
    assert np.allclose(Q.T @ Q, np.eye(4), atol=1e-12)


def test_same_span_and_order():
    A = rng.normal(size=(6, 3))
    Q = sub.gram_schmidt(A)
    assert np.allclose(Q @ (Q.T @ A), A, atol=1e-10), "columns of A must lie in span(Q)"
    assert np.allclose(Q[:, 0], A[:, 0] / np.linalg.norm(A[:, 0])), "first column is a1 normalized"
    assert abs(Q[:, 1] @ A[:, 0]) < 1e-12


def test_dependent_columns_raise():
    A = rng.normal(size=(5, 2))
    A = np.column_stack([A, A[:, 0] - 2 * A[:, 1]])
    try:
        sub.gram_schmidt(A)
    except ValueError:
        return
    raise AssertionError("expected ValueError for a dependent column")


def test_stays_orthogonal_on_nearly_parallel_columns():
    # Condition number about 1e7: classical Gram-Schmidt loses orthogonality
    # (error near kappa^2 * eps), the modified form keeps it near kappa * eps.
    n = 8
    U, _ = np.linalg.qr(rng.normal(size=(30, n)))
    V, _ = np.linalg.qr(rng.normal(size=(n, n)))
    A = U @ np.diag(np.logspace(0, -7, n)) @ V.T
    Q = sub.gram_schmidt(A)
    err = np.linalg.norm(Q.T @ Q - np.eye(n))
    assert err < 1e-6, f"orthogonality error {err:.2e}; use the modified update"

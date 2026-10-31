import numpy as np
import sub


def test_normal_equations_lose_digits():
    A = sub.vandermonde(100, 12)
    assert 1e7 < np.linalg.cond(A) < 1e9
    x_true = np.ones(12)
    b = A @ x_true
    qr = sub.relative_error(sub.solve_qr(A, b), x_true)
    ne = sub.relative_error(sub.solve_normal(A, b), x_true)
    assert qr < 1e-7 and ne > 1e-2, (qr, ne)


def test_well_conditioned_both_fine():
    A = np.random.default_rng(0).standard_normal((100, 12))
    b = A @ np.ones(12)
    assert sub.relative_error(sub.solve_normal(A, b), np.ones(12)) < 1e-12
    assert sub.relative_error(sub.solve_qr(A, b), np.ones(12)) < 1e-12

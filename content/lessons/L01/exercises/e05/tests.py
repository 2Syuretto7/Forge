import numpy as np
import sub

rng = np.random.default_rng(5)
A = rng.normal(size=(40, 6))
x_true = rng.normal(size=6)
b = A @ x_true + 0.1 * rng.normal(size=40)
ref, *_ = np.linalg.lstsq(A, b, rcond=None)


def test_normal_equations_solution():
    x = sub.lstsq_normal(A, b)
    assert x.shape == (6,)
    assert np.allclose(x, ref, atol=1e-10)


def test_qr_solution():
    assert np.allclose(sub.lstsq_qr(A, b), ref, atol=1e-10)


def test_report_values():
    rep = sub.residual_report(A, b, ref)
    assert abs(rep["residual_norm"] - np.linalg.norm(A @ ref - b)) < 1e-10
    assert rep["max_orthogonality"] < 1e-10, "the least-squares residual is orthogonal to the columns"


def test_report_detects_a_bad_fit():
    rep = sub.residual_report(A, b, ref + 0.5)
    assert rep["max_orthogonality"] > 1e-3


def test_exact_fit_has_zero_residual():
    b2 = A @ x_true
    assert sub.residual_report(A, b2, sub.lstsq_qr(A, b2))["residual_norm"] < 1e-10

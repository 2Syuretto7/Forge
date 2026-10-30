import numpy as np
import sub

rng = np.random.default_rng(5)
A = rng.normal(size=(40, 6))
x_true = rng.normal(size=6)
b = A @ x_true + 0.1 * rng.normal(size=40)
ref, *_ = np.linalg.lstsq(A, b, rcond=None)


def test_both_methods():
    assert np.allclose(sub.lstsq_normal(A, b), ref, atol=1e-10)
    assert np.allclose(sub.lstsq_qr(A, b), ref, atol=1e-10)


def test_report():
    rep = sub.residual_report(A, b, ref)
    assert abs(rep["residual_norm"] - np.linalg.norm(A @ ref - b)) < 1e-10
    assert rep["max_orthogonality"] < 1e-10
    assert sub.residual_report(A, b, ref + 0.5)["max_orthogonality"] > 1e-3

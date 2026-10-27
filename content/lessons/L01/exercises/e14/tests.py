import numpy as np
import sub

rng = np.random.default_rng(14)


def test_hilbert_matrix():
    H = sub.hilbert(3, np.float64)
    assert np.allclose(H, [[1, 1 / 2, 1 / 3], [1 / 2, 1 / 3, 1 / 4], [1 / 3, 1 / 4, 1 / 5]])
    assert sub.hilbert(3, np.float32).dtype == np.float32


def test_gauss_solve_is_correct_and_keeps_dtype():
    A = rng.normal(size=(6, 6)) + 3 * np.eye(6)
    b = rng.normal(size=6)
    assert np.allclose(sub.gauss_solve(A, b), np.linalg.solve(A, b), atol=1e-10)
    x32 = sub.gauss_solve(A.astype(np.float32), b.astype(np.float32))
    assert x32.dtype == np.float32, "the solver must stay in float32 for float32 input"


def test_gauss_solve_needs_pivoting():
    A = np.array([[1e-20, 1.0], [1.0, 1.0]])
    x = sub.gauss_solve(A, np.array([1.0, 2.0]))
    assert np.allclose(x, [1.0, 1.0], atol=1e-12), f"got {x}; did you pivot?"


def test_float32_breaks_where_float64_survives():
    e32 = sub.hilbert_error(6, np.float32)
    e64 = sub.hilbert_error(6, np.float64)
    assert e32 > 1e-2, f"float32 error {e32:.2e} should be large"
    assert e64 < 1e-7, f"float64 error {e64:.2e} should be small"
    assert sub.hilbert_error(12, np.float64) > 100 * e64, "error grows with the condition number"


def test_qr_beats_normal_equations():
    U = np.linalg.qr(rng.normal(size=(50, 6)))[0]
    V = np.linalg.qr(rng.normal(size=(6, 6)))[0]
    A = U @ np.diag(np.logspace(0, -6, 6)) @ V.T
    out = sub.normal_vs_qr(A, rng.normal(size=6))
    assert out["qr"] < 1e-7, f"QR error {out['qr']:.2e}"
    assert out["normal"] > 100 * out["qr"], f"normal {out['normal']:.2e} vs QR {out['qr']:.2e}"

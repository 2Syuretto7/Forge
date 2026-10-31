import numpy as np
import sub


def test_plain_cg_fails():
    rng = np.random.default_rng(0)
    A = sub.make_nonsymmetric(100, rng)
    b = rng.standard_normal(100)
    res = sub.cg_residuals(A, b, 300)
    assert min(res) > 1e-2, min(res)
    x, k = sub.cgnr(A, b)
    assert np.linalg.norm(A @ x - b) < 1e-8 * np.linalg.norm(b) and k < 5000


def test_symmetric_case_still_works():
    rng = np.random.default_rng(1)
    G = rng.standard_normal((60, 60))
    A = G @ G.T / 60 + np.eye(60)
    assert sub.cg_residuals(A, np.ones(60), 60)[-1] < 1e-8

import numpy as np
import sub


def test_jacobi_rescues_cg():
    rng = np.random.default_rng(0)
    A = sub.badly_scaled(300, rng)
    b = rng.standard_normal(300)
    assert np.linalg.cond(A) > 1e7
    assert sub.jacobi_condition(A) < 20
    _, plain = sub.pcg(A, b, np.ones(300), max_iter=2000)
    x, pre = sub.pcg(A, b, 1 / np.diag(A))
    assert plain == 2000 and pre < 100, (plain, pre)
    assert np.linalg.norm(A @ x - b) <= 1e-8 * np.linalg.norm(b)


def test_identity_preconditioner_is_cg():
    rng = np.random.default_rng(1)
    G = rng.standard_normal((50, 50))
    A = G @ G.T / 50 + np.eye(50)
    b = rng.standard_normal(50)
    x, k = sub.pcg(A, b, np.ones(50))
    assert np.allclose(A @ x, b, atol=1e-7) and k <= 50

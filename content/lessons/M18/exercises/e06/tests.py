import numpy as np
import sub

rng = np.random.default_rng(12)
M = rng.normal(size=(4, 4))
S = M @ M.T + np.eye(4)


def test_grad_quadratic():
    H = sub.hessian_from_grad(lambda x: S @ x, rng.normal(size=4))
    assert np.allclose(H, S, atol=1e-8) and sub.is_local_min(H)
    assert abs(sub.curvature_bound(H) - np.linalg.eigvalsh(S).max()) < 1e-6


def test_grad_saddle():
    H = sub.hessian_from_grad(lambda v: np.array([2 * v[0], -2 * v[1]]), np.zeros(2))
    assert not sub.is_local_min(H)


def test_grad_rosenbrock():
    def grad(v):
        x, y = v
        return np.array([-2 * (1 - x) - 400 * x * (y - x * x), 200 * (y - x * x)])
    H = sub.hessian_from_grad(grad, np.array([1.0, 1.0]))
    assert np.allclose(H, [[802, -400], [-400, 200]], atol=1e-4)
    assert sub.is_local_min(H) and sub.curvature_bound(H) > 1000

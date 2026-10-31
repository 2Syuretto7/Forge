import numpy as np
import sub

A = np.array([[3.0, 1.0, 0.0], [1.0, 2.0, -0.5], [0.0, -0.5, 1.0]])


def lse(x):
    m = np.max(x)
    return float(m + np.log(np.sum(np.exp(x - m))))


def test_grad_hessian():
    x = np.array([0.3, -1.0, 0.5])
    assert np.allclose(sub.hessian_fd(lambda v: 0.5 * v @ A @ v, x), A, atol=1e-6)
    p = np.exp(x - lse(x))
    assert np.allclose(sub.hessian_fd(lse, x), np.diag(p) - np.outer(p, p), atol=1e-6)


def test_classification():
    rng = np.random.default_rng(2)
    pts = rng.normal(size=(20, 3))
    assert sub.convex_on_samples(lse, pts)
    assert sub.convex_on_samples(lambda v: 0.5 * v @ A @ v, pts)
    assert not sub.convex_on_samples(lambda v: float(v[0] * v[1]), pts)
    w = lambda v: float(v[0] ** 4 - v[0] ** 2)
    assert sub.convex_on_samples(w, [np.array([1.0]), np.array([-2.0])])
    assert not sub.convex_on_samples(w, [np.array([0.0])])
    assert abs(sub.min_eigenvalue(np.array([[2.0, 1.0], [1.0, 2.0]])) - 1) < 1e-12

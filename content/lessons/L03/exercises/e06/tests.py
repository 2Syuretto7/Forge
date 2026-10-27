import numpy as np
import sub

rng = np.random.default_rng(6)
A = rng.normal(size=(3, 5))
b = rng.normal(size=3)
x = rng.normal(size=5)


def _numjac(f, x, h=1e-6):
    m = f(x).size
    J = np.zeros((m, x.size))
    for j in range(x.size):
        e = np.zeros_like(x)
        e[j] = h
        J[:, j] = (f(x + e) - f(x - e)) / (2 * h)
    return J


def test_full_jacobian_matches_finite_differences():
    J = sub.full_jacobian(A, b, x)
    assert J.shape == (3, 5)
    assert np.allclose(J, _numjac(lambda z: sub.forward(A, b, z), x), atol=1e-8)


def test_jvp_matches_jacobian():
    v = rng.normal(size=5)
    assert np.allclose(sub.jvp(A, b, x, v), sub.full_jacobian(A, b, x) @ v)


def test_grad_vjp_matches_jacobian_transpose():
    u = rng.normal(size=3)
    g = sub.vjp(A, b, x, u)
    assert g.shape == (5,)
    num = _numjac(lambda z: np.array([u @ sub.forward(A, b, z)]), x)[0]
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_dot_product_identity():
    for _ in range(10):
        u, v = rng.normal(size=3), rng.normal(size=5)
        assert abs(u @ sub.jvp(A, b, x, v) - sub.vjp(A, b, x, u) @ v) < 1e-12

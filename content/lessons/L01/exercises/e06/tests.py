import numpy as np
import sub

rng = np.random.default_rng(6)
A = rng.normal(size=(20, 5))
b = rng.normal(size=20)


def _numgrad(f, x, h=1e-6):
    g = np.zeros_like(x)
    for i in range(x.size):
        e = np.zeros_like(x)
        e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def test_loss_value():
    x = rng.normal(size=5)
    assert abs(sub.loss(x, A, b) - np.sum((A @ x - b) ** 2)) < 1e-10


def test_grad_matches_finite_differences():
    x = rng.normal(size=5)
    g = sub.grad(x, A, b)
    n = _numgrad(lambda z: sub.loss(z, A, b), x)
    rel = np.linalg.norm(g - n) / (np.linalg.norm(g) + np.linalg.norm(n))
    assert g.shape == (5,)
    assert rel < 1e-5, f"relative error {rel:.2e}"


def test_grad_vanishes_at_the_solution():
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.linalg.norm(sub.grad(x, A, b)) < 1e-9


def test_gradient_descent_converges():
    x = sub.gd_solve(A, b, 3000)
    ref, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.allclose(x, ref, atol=1e-6), f"max error {np.max(np.abs(x - ref)):.2e}"

import numpy as np
import sub

rng = np.random.default_rng(1)
M = rng.normal(size=(5, 5))
A = M @ M.T + 0.5 * np.eye(5)
b = rng.normal(size=5)


def test_value():
    x = rng.normal(size=5)
    f, _ = sub.quad_fg(A, b, x)
    assert abs(f - (0.5 * x @ A @ x - b @ x)) < 1e-10


def test_grad_quadratic():
    x = rng.normal(size=5)
    _, g = sub.quad_fg(A, b, x)
    num = np.zeros(5)
    for i in range(5):
        e = np.zeros(5)
        e[i] = 1e-6
        num[i] = (sub.quad_fg(A, b, x + e)[0] - sub.quad_fg(A, b, x - e)[0]) / 2e-6
    assert np.allclose(g, num, atol=1e-6)


def test_iterates():
    x0 = np.ones(5)
    xs = sub.gd(lambda x: A @ x - b, x0, 0.01, 7)
    assert xs.shape == (8, 5)
    assert np.allclose(xs[0], x0) and np.all(x0 == 1.0)
    assert np.allclose(xs[1], x0 - 0.01 * (A @ x0 - b))


def test_converges_to_solution():
    lr = 1.0 / np.linalg.eigvalsh(A)[-1]
    xs = sub.gd(lambda x: sub.quad_fg(A, b, x)[1], np.zeros(5), lr, 3000)
    assert np.allclose(xs[-1], np.linalg.solve(A, b), atol=1e-6)

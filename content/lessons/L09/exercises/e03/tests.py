import numpy as np
import sub

D = np.diag(np.linspace(1.0, 100.0, 20))
grad = lambda x: D @ x
x0 = np.ones(20)


def test_beta_zero_is_gd():
    assert np.allclose(sub.heavy_ball(grad, x0, 0.01, 0.0, 30), sub.gd(grad, x0, 0.01, 30))


def test_two_steps():
    xs = sub.heavy_ball(grad, x0, 0.01, 0.5, 2)
    v1 = grad(x0)
    x1 = x0 - 0.01 * v1
    v2 = 0.5 * v1 + grad(x1)
    assert np.allclose(xs[1], x1) and np.allclose(xs[2], x1 - 0.01 * v2)


def test_tuned_values():
    lr, beta = sub.tuned_heavy_ball(np.diag([1.0, 100.0]))
    assert abs(lr - 4 / 121) < 1e-12 and abs(beta - (9 / 11) ** 2) < 1e-12


def test_faster_than_gd():
    lr, beta = sub.tuned_heavy_ball(D)
    hb = np.linalg.norm(sub.heavy_ball(grad, x0, lr, beta, 100)[-1])
    plain = np.linalg.norm(sub.gd(grad, x0, 2 / 101, 100)[-1])
    assert hb < 1e-5, hb
    assert plain > 0.1, plain

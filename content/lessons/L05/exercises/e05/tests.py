import numpy as np
import sub


def test_grad_rosenbrock():
    for p in [np.array([-1.2, 1.0]), np.array([0.3, -0.4]), np.array([2.0, 3.5])]:
        _, g = sub.rosenbrock_fg(p)
        num = np.array([(sub.rosenbrock_fg(p + e)[0] - sub.rosenbrock_fg(p - e)[0]) / 2e-6 for e in np.eye(2) * 1e-6])
        assert np.allclose(g, num, rtol=1e-6, atol=1e-6)


def test_minimum():
    f, g = sub.rosenbrock_fg(np.array([1.0, 1.0]))
    assert f == 0 and np.allclose(g, 0)
    f, g = sub.rosenbrock_fg(np.array([2.0, 4.0]), a=2.0)
    assert f == 0 and np.allclose(g, 0)


def test_first_step_is_lr():
    g = np.array([1e-3, -5.0, 300.0])
    x1 = sub.Adam(0.01).step(np.zeros(3), g)
    assert np.allclose(x1, -0.01 * np.sign(g), rtol=1e-4)


def test_without_correction_first_step():
    x1 = sub.Adam(0.01, bias_correction=False).step(np.zeros(1), np.array([2.0]))
    assert abs(x1[0] + 0.01 * 0.1 / np.sqrt(0.001)) < 1e-6


def test_scale_invariance():
    D = np.diag([1.0, 50.0])
    runs = []
    for c in [1.0, 1000.0]:
        opt = sub.Adam(0.05, eps=0.0)
        x = np.array([1.0, 1.0])
        for _ in range(60):
            x = opt.step(x, c * (D @ x))
        runs.append(x)
    assert np.allclose(runs[0], runs[1], rtol=1e-9, atol=1e-12)


def test_solves_rosenbrock():
    opt = sub.Adam(0.02)
    p = np.array([-1.5, 2.0])
    for _ in range(5000):
        p = opt.step(p, sub.rosenbrock_fg(p)[1])
    assert np.allclose(p, [1.0, 1.0], atol=1e-4), p

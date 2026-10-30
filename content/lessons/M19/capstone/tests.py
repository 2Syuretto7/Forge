import math
import numpy as np
import sub


def ref_target(x):
    a, b, c = x
    s = a * b + math.sin(c)
    t = math.exp(-s * s / 4)
    u = math.log(1 + a * a) / (1 + t)
    v = sum(u ** k / k for k in range(1, 4))
    w = math.sqrt(a * a + b * b + 1) if a > 0 else math.cos(b) + 2
    y = v * w + math.tanh(c - a)
    return y / (1 + b * b) + 3 * t


def ref_grad(x):
    g = np.zeros(3)
    for j in range(3):
        def d(h):
            xp, xm = list(x), list(x)
            xp[j] += h
            xm[j] -= h
            return (ref_target(xp) - ref_target(xm)) / (2 * h)
        g[j] = (4 * d(1e-3) - d(2e-3)) / 3
        g[j] = (16 * ((4 * d(5e-4) - d(1e-3)) / 3) - g[j]) / 15
    return g


POINTS = [[0.7, -1.2, 0.4], [1.5, 0.3, -0.8], [-0.6, 0.9, 1.1], [-1.4, -0.5, 0.2]]


def test_target_on_floats():
    for p in POINTS:
        assert abs(sub.target(p) - ref_target(p)) < 1e-12


def test_grad_forward_and_reverse_match_reference():
    for p in POINTS:
        gf, gr = sub.grad_forward(sub.target, p), sub.grad_reverse(sub.target, p)
        r = ref_grad(p)
        assert gf.shape == (3,) and gr.shape == (3,)
        assert np.max(np.abs(gf - r)) < 1e-9 and np.max(np.abs(gr - r)) < 1e-9, (p, gf, gr, r)
        assert np.max(np.abs(gf - gr)) < 1e-12


def test_grad_check_reports_agreement():
    for p in POINTS:
        assert sub.check(sub.target, p) < 1e-8


def test_fd_grad_simple():
    assert np.allclose(sub.fd_grad(lambda v: v[0] ** 2 + 3 * v[1], [2.0, 5.0]), [4.0, 3.0], atol=1e-8)

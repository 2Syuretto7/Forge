import math
import numpy as np
import sub


def trap(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (b - a) / n * (y.sum() - (y[0] + y[-1]) / 2)


def simp(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return (b - a) / n / 3 * np.sum(w * f(x))


def test_one_step_is_simpson():
    assert abs(sub.richardson(trap(np.exp, 0, 1, 8), trap(np.exp, 0, 1, 16), 2) - simp(np.exp, 0, 1, 16)) < 1e-14


def test_romberg():
    assert abs(sub.romberg(np.exp, 0, 1, 7) - (math.e - 1)) < 1e-14
    assert abs(sub.romberg(np.sin, 0, math.pi, 8) - 2) < 1e-13

import math
import numpy as np
import sub


def slow_rope(x, m, base=10000):
    out = []
    for j in range(len(x) // 2):
        w = base ** (-2 * j / len(x))
        a, b = x[2 * j], x[2 * j + 1]
        out += [a * math.cos(m * w) - b * math.sin(m * w), a * math.sin(m * w) + b * math.cos(m * w)]
    return out


def test_matches_the_loop_version():
    X = np.random.default_rng(0).normal(size=(5, 8))
    pos = np.array([0, 1, 5, 100, 2047])
    Y = sub.rope_batch(X, pos)
    for i in range(5):
        assert np.allclose(Y[i], slow_rope(list(X[i]), int(pos[i])), atol=1e-12)


def test_relative_property_at_scale():
    assert sub.relative_check(64, 1000) < 1e-9

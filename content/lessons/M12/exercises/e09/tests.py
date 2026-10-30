import numpy as np
import sub

rng = np.random.default_rng(9)


def test_puzzle_points():
    w0, w1 = sub.line_fit([0, 1, 2], [0, 1, 1])
    assert np.isclose(w0, 1 / 6) and np.isclose(w1, 0.5)


def test_agree_and_check():
    x = rng.uniform(0, 10, 50)
    y = 3 - 0.7 * x + rng.normal(size=50)
    a = sub.line_fit(x, y)
    c = sub.centered_fit(x, y)
    assert np.allclose(a, c) and np.allclose(a, np.polyfit(x, y, 1)[::-1])
    s, sx = sub.residual_checks(x, y, *a)
    assert abs(s) < 1e-9 and abs(sx) < 1e-8

import numpy as np
import sub

rng = np.random.default_rng(7)


def test_design():
    assert np.allclose(sub.design([2.0, 3.0], 2), [[1, 2, 4], [1, 3, 9]])


def test_fit_matches_numpy():
    x = np.linspace(-1, 1, 50)
    y = np.cos(2 * x) + 0.01 * rng.normal(size=50)
    c = sub.polyfit_ls(x, y, 4)
    assert np.allclose(c, np.polyfit(x, y, 4)[::-1], atol=1e-8)
    assert np.allclose(sub.polyval(c, x), np.polyval(np.polyfit(x, y, 4), x), atol=1e-8)


def test_exact_recovery():
    x = np.linspace(0, 2, 30)
    c0 = np.array([1.0, -2.0, 0.5, 0.25])
    assert np.allclose(sub.polyfit_ls(x, sub.polyval(c0, x), 3), c0, atol=1e-9)

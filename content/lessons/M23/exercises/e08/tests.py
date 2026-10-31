import numpy as np
import sub


def walk(n, q, r, seed):
    rng = np.random.default_rng(seed)
    x = np.cumsum(np.sqrt(q) * rng.standard_normal(n))
    return x, x + np.sqrt(r) * rng.standard_normal(n)


def test_beats_raw_measurements():
    x, z = walk(5000, 0.01, 1.0, 12)
    m, p = sub.kalman_1d(z, 0.01, 1.0, 0.0, 1.0)
    raw = np.sqrt(np.mean((z - x) ** 2))
    filt = np.sqrt(np.mean((m - x)[100:] ** 2))
    assert filt < 0.4 * raw, (filt, raw)
    assert abs(filt**2 / sub.steady_variance(0.01, 1.0) - 1) < 0.15


def test_variance_settles():
    _, p = sub.kalman_1d(np.zeros(200), 0.5, 2.0, 0.0, 100.0)
    s = sub.steady_variance(0.5, 2.0)
    assert abs(p[-1] - s) < 1e-12
    assert abs(s - (s + 0.5) * 2.0 / (s + 0.5 + 2.0)) < 1e-12


def test_first_step():
    m, p = sub.kalman_1d([4.0], 1.0, 2.0, 0.0, 1.0)
    assert abs(m[0] - 2.0) < 1e-12 and abs(p[0] - 1.0) < 1e-12

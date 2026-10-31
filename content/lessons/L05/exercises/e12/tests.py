import numpy as np
import sub


def test_closed_form():
    assert abs(sub.uncorrected_factor(1) - 0.1 / np.sqrt(0.001)) < 1e-12
    f = sub.uncorrected_factor(np.array([1, 100]))
    assert f.shape == (2,) and 3.2 < f[1] < 3.3


def test_peak():
    t, f = sub.peak()
    assert t == 12 and abs(f - 6.5685) < 1e-3
    t2, f2 = sub.peak(0.9, 0.99)
    ts = np.arange(1, 10001)
    ref = (1 - 0.9 ** ts) / np.sqrt(1 - 0.99 ** ts)
    assert t2 == int(ts[np.argmax(ref)]) and abs(f2 - ref.max()) < 1e-12


def test_measured_matches_closed_form():
    for t in [1, 5, 12, 100]:
        assert abs(sub.measured_factor(t) - sub.uncorrected_factor(t)) < 1e-9 * sub.uncorrected_factor(t)
    assert abs(sub.measured_factor(7, g=-3.0) - sub.uncorrected_factor(7)) < 1e-9

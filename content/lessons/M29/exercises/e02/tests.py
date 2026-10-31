import numpy as np
import sub


def test_fit_on_a_noisy_geometric_sequence():
    rng = np.random.default_rng(2)
    k = np.arange(200)
    e = 3.0 * 0.95**k * np.exp(rng.normal(0, 0.05, 200))
    assert abs(sub.fit_rate(e, 20, 180) - 0.95) < 0.002


def test_transient_is_skipped():
    k = np.arange(300)
    e = 0.5**k + 1e-3 * 0.98**k
    assert abs(sub.fit_rate(e, 100, 300) - 0.98) < 1e-6
    assert sub.fit_rate(e, 0, 10) < 0.6


def test_helpers():
    assert sub.iterations_for(0.99, 1e6) == 1375
    assert abs(sub.half_life(0.99) - 68.97) < 0.01

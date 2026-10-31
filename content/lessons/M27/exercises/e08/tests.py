import numpy as np
import sub

p = np.array([0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05])
H = float(-np.sum(p * np.log(p)))


def test_plugin_on_known_sample():
    assert abs(sub.plugin_entropy(np.array([0, 0, 1, 1]), 3) - np.log(2)) < 1e-12
    assert abs(sub.miller_madow(np.array([0, 0, 1, 1]), 3) - (np.log(2) + 1 / 8)) < 1e-12


def test_plugin_is_biased_low_and_correction_helps():
    a, b = sub.average_estimates(p, 20, 4000, seed=1)
    assert a < H - 0.1, f"plug-in average {a:.3f} vs true {H:.3f}"
    assert abs(b - H) < abs(a - H) / 2


def test_bias_vanishes_with_more_data():
    a, _ = sub.average_estimates(p, 2000, 200, seed=2)
    assert abs(a - H) < 0.01

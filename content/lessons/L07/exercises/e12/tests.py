import numpy as np
import sub


def test_unit_std_explodes():
    r = sub.activation_rms(10, 256, 1.0, seed=0)
    growth = (r[-1] / r[0]) ** (1 / 9)
    assert abs(growth / sub.predicted_growth(256, 1.0) - 1) < 0.1, growth
    assert r[-1] > 1e9


def test_he_init_is_stable():
    r = sub.activation_rms(10, 256, np.sqrt(2 / 256), seed=0)
    assert 0.3 < r[-1] < 3, r[-1]
    assert abs(sub.predicted_growth(256, np.sqrt(2 / 256)) - 1) < 1e-12


def test_small_std_vanishes():
    r = sub.activation_rms(10, 256, 0.01, seed=0)
    assert r[-1] < 1e-6

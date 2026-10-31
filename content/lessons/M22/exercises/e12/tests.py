import numpy as np
import sub


def rate(m):
    return m[-1] ** (1 / len(m))


def test_preserving_scales_hold_for_fifty_layers():
    for act in ("linear", "relu"):
        m = sub.layer_second_moments(50, 128, sub.preserving_scale(act), act)
        assert len(m) == 50
        assert 0.9 < rate(m) < 1.1, (act, m[-1])


def test_wrong_scales_explode_or_vanish():
    m = sub.layer_second_moments(50, 128, 1.2, "linear")
    assert m[-1] > 1e6 and abs(rate(m) / sub.predicted_factor(1.2, "linear", 1) - 1) < 0.1
    m = sub.layer_second_moments(50, 128, 1.0, "relu")
    assert m[-1] < 1e-10 and abs(rate(m) / sub.predicted_factor(1.0, "relu", 1) - 1) < 0.1


def test_predicted_factor():
    assert sub.predicted_factor(1.0, "linear", 10) == 1.0
    assert abs(sub.predicted_factor(np.sqrt(2), "relu", 10) - 1) < 1e-12
    assert abs(sub.predicted_factor(1.2, "linear", 2) - 1.44**2) < 1e-12

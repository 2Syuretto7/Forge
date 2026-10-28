import numpy as np
import sub


def test_adamw_independent_of_scale():
    target = sub.predicted_adamw(0.01, 0.1, 1000)
    assert abs(target - 0.999 ** 1000) < 1e-12
    for s in [10.0, 1.0, 0.1, 0.01]:
        assert abs(sub.simulate("adamw", s) - target) < 0.02, s


def test_l2_depends_on_scale():
    assert sub.simulate("adam_l2", 10.0) > 0.85
    assert abs(sub.simulate("adam_l2", 0.01)) < 0.01


def test_l2_prediction_for_large_gradients():
    for s in [10.0, 30.0]:
        assert abs(sub.simulate("adam_l2", s) - sub.predicted_l2_noisy(s, 0.01, 0.1, 1000)) < 0.03, s

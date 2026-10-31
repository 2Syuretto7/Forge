import numpy as np
import sub


def test_first_step_factor():
    assert abs(sub.first_step(0.9, 0.999) - 3.1623) < 1e-4
    assert sub.first_step(0.99, 0.5) < 0.02


def test_early_steps_too_long():
    raw = sub.step_lengths(2.0, 0.01, 6000, bias_correction=False)
    fixed = sub.step_lengths(2.0, 0.01, 6000)
    assert np.allclose(fixed, 0.01)
    assert abs(raw[0] - 0.0316) < 1e-3
    assert np.sum(raw[:100]) > 2 * np.sum(fixed[:100])
    assert abs(raw[-1] / fixed[-1] - 1) < 0.01

import math
import numpy as np
import sub


def test_uncorrected_steps_too_large():
    u = sub.uncorrected_step_sizes(0.3, 5000)
    c = sub.corrected_step_sizes(0.3, 5000)
    assert np.allclose(c, 1.0)
    assert abs(u[0] - 0.1 / math.sqrt(0.001)) < 1e-9
    assert np.sum(u > 2) > 50 and abs(u[-1] - 1) < 0.01
    assert sub.peak_ratio(0.9, 0.999) > 3

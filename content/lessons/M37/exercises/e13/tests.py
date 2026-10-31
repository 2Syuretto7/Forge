import math
import numpy as np
import sub


def test_step_size():
    rng = np.random.default_rng(0)
    x = sub.em_ou(0.0, 2.0, 1.0, 0.25, 200, 40000, rng)
    assert abs(x.var() / sub.em_stationary_var(2.0, 1.0, 0.25) - 1) < 0.04
    assert abs(sub.em_stationary_var(2.0, 1.0, 0.25) / 0.25 - 4 / 3) < 1e-12
    y = sub.exact_ou(0.0, 2.0, 1.0, 0.25, 200, 40000, rng)
    assert abs(y.var() / 0.25 - 1) < 0.04
    z = sub.em_ou(1.0, 2.0, 1.0, 1.1, 2000, 100, rng)
    assert not np.all(np.isfinite(z)) or np.max(np.abs(z)) > 1e100
    assert sub.em_stationary_var(2.0, 1.0, 1.0) == math.inf

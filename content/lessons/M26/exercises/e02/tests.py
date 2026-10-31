import numpy as np
import sub


def test_epsilons():
    assert sub.machine_epsilon(np.float64) == 2.0**-52
    assert sub.machine_epsilon(np.float32) == 2.0**-23
    assert sub.machine_epsilon(np.float16) == 2.0**-10
    assert sub.unit_roundoff(np.float64) == 2.0**-53


def test_stall_points():
    assert sub.stall_point(np.float16) == 2048
    assert sub.stall_point(np.float32) == 2**24
    assert sub.stall_point(np.float64) == 2**53


def test_rounding_bound():
    x = 0.1 + 0.2
    assert abs(x - 0.3) / 0.3 <= 2 * sub.unit_roundoff(np.float64)

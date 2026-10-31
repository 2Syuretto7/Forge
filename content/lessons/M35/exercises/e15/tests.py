import math
import numpy as np
import sub


def test_few_runs_need_student():
    rng = np.random.default_rng(0)
    u0 = math.log(1e4)
    small_z = sub.coverage(5, 1.96, u0, 4000, rng)
    small_t = sub.coverage(5, 3.182, u0, 4000, rng)
    big_z = sub.coverage(50, 1.96, u0, 2000, rng)
    assert small_z < 0.9 and abs(small_t - 0.95) < 0.02 and abs(big_z - 0.95) < 0.025, (small_z, small_t, big_z)


def test_line_fit():
    a, b, s = sub.line_fit([0, 1, 2, 3], [1, 3, 5, 7])
    assert abs(a - 1) < 1e-12 and abs(b - 2) < 1e-12 and s < 1e-12

import math
import numpy as np
import sub


def test_ulps():
    assert sub.ulps_between(0.1 + 0.2, 0.3) == 1
    assert sub.ulps_between(1.0, float(np.nextafter(1.0, 2.0))) == 1
    assert sub.ulps_between(-0.0, 0.0) == 0
    assert sub.ulps_between(-5e-324, 5e-324) == 2
    assert sub.ulps_between(1.0, 2.0) == 2**52


def test_close():
    assert not (0.1 + 0.2 == 0.3) and sub.close(0.1 + 0.2, 0.3)
    assert not sub.close(1e-20, 0.0) and sub.close(1e-20, 0.0, abs_tol=1e-12)
    for a, b in [(1.0, 1.0 + 1e-10), (100.0, 100.0 + 1e-6), (3.0, 3.1)]:
        assert sub.close(a, b) == math.isclose(a, b)
    assert abs(sub.relative_error(1.01, 1.0) - 0.01) < 1e-12

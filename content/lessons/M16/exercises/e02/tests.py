import math
import sub


def test_sqrt2():
    r, k = sub.bisect(lambda x: x * x - 2, 0.0, 2.0, 1e-12)
    assert abs(r - math.sqrt(2)) < 1e-12
    assert k == sub.predicted_iterations(0.0, 2.0, 1e-12)


def test_other_roots():
    r, _ = sub.bisect(math.cos, 0.0, 3.0)
    assert abs(r - math.pi / 2) < 1e-11
    try:
        sub.bisect(lambda x: x * x + 1, -1.0, 1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

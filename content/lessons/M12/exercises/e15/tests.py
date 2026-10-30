import numpy as np
import sub

rng = np.random.default_rng(15)


def test_far_point():
    x = np.append(rng.uniform(0, 1, 20), 10.0)
    h = sub.leverages(sub.line_design(x))
    assert h[-1] > 0.9 and np.all(h[:-1] < 0.2)
    y = 2 * x + 0.1 * rng.normal(size=21)
    y[-1] += 5
    assert abs(sub.influence(x, y, 20)) > 10 * abs(sub.influence(x, y, 0))


def test_invariant_leverage_sums_to_columns():
    for _ in range(50):
        m = int(rng.integers(3, 30))
        n = int(rng.integers(1, min(m, 6) + 1))
        h = sub.leverages(rng.normal(size=(m, n)))
        assert np.all(h >= -1e-12) and np.all(h <= 1 + 1e-12)
        assert np.isclose(h.sum(), n)

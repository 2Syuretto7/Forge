import numpy as np
import sub

STEP = 2.0 ** -7


def test_unbiased():
    rng = np.random.default_rng(0)
    x = np.full(20000, 1.0 + 0.3 * STEP)
    r = sub.stochastic_round(x, STEP, rng)
    assert set(np.unique(r)) == {1.0, 1.0 + STEP}
    assert abs(r.mean() - x[0]) < 3e-4


def test_small_updates():
    assert sub.accumulate(1.0, 1e-3, 1000, STEP, "nearest") == 1.0
    runs = [sub.accumulate(1.0, 1e-3, 1000, STEP, "stochastic", np.random.default_rng(s)) for s in range(10)]
    assert abs(np.mean(runs) - 2.0) < 0.05

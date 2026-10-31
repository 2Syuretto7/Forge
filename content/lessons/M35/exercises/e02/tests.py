import numpy as np
import sub


def test_recovers_power_law():
    rng = np.random.default_rng(0)
    x = np.logspace(0, 3, 40)
    y = 3.0 * x**-0.4 * np.exp(0.05 * rng.standard_normal(40))
    A, alpha = sub.fit_loglog(x, y)
    assert abs(alpha - 0.4) < 0.02 and abs(A / 3 - 1) < 0.1
    assert sub.loglog_r2(x, y) > 0.99


def test_good_r2_wrong_law():
    x = np.logspace(0, 2, 20)
    y = 0.5 + 2.0 * x**-0.5
    _, alpha = sub.fit_loglog(x, y)
    assert sub.loglog_r2(x, y) > 0.98 and alpha < 0.3
    assert np.allclose(sub.predict_loglog(2.0, 1.0, [1, 2]), [2.0, 1.0])

import numpy as np
import sub

rng = np.random.default_rng(6)
x = rng.uniform(-1, 1, 40)
y = np.sin(np.pi * x) + 0.3 * rng.normal(size=40)
xt = rng.uniform(-1, 1, 5000)
yt = np.sin(np.pi * xt) + 0.3 * rng.normal(size=5000)


def _test_err(d):
    c = np.linalg.lstsq(np.vander(x, d + 1, increasing=True), y, rcond=None)[0]
    return np.mean((np.vander(xt, d + 1, increasing=True) @ c - yt) ** 2)


def test_selected_model_is_near_the_best():
    degrees = list(range(0, 13))
    d = sub.select_degree(x, y, degrees, 5, 0)
    c = sub.refit(x, y, d)
    err = np.mean((np.vander(xt, d + 1, increasing=True) @ c - yt) ** 2)
    best = min(_test_err(k) for k in degrees)
    assert err < 1.2 * best, (d, err, best)

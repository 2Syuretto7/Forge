import numpy as np
import sub


def fit_and_cov():
    rng = np.random.default_rng(0)
    x = np.logspace(0, 2, 30)
    th = np.array([1.7, 2.0, 0.5])
    y = th[0] + th[1] * x**-th[2] + 0.01 * rng.standard_normal(30)
    for _ in range(30):
        p = x ** -th[2]
        J = np.stack([np.ones(30), p, -th[1] * p * np.log(x)], 1)
        r = y - (th[0] + th[1] * p)
        th = th + np.linalg.lstsq(J, r, rcond=None)[0]
    p = x ** -th[2]
    J = np.stack([np.ones(30), p, -th[1] * p * np.log(x)], 1)
    r = y - (th[0] + th[1] * p)
    return th, (r @ r) / 27 * np.linalg.inv(J.T @ J)


def test_grad_prediction():
    th = np.array([1.3, 2.2, 0.6])
    h = 1e-6
    for x0 in (2.0, 50.0, 3000.0):
        g = sub.grad_prediction(th, x0)
        for j in range(3):
            e = np.zeros(3)
            e[j] = h
            num = (sub.prediction(th + e, x0) - sub.prediction(th - e, x0)) / (2 * h)
            assert abs(num - g[j]) < 1e-7


def test_band_widens_outside():
    th, cov = fit_and_cov()
    inside = max(sub.prediction_se(th, cov, x) for x in np.logspace(0, 2, 20))
    for x0 in (1e3, 1e4):
        assert sub.prediction_se(th, cov, x0) > inside
    lo, hi = sub.band(th, cov, [10.0, 1e4])
    assert np.all(lo < hi) and (hi - lo)[1] > (hi - lo)[0]

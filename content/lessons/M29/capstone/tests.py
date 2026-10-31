import math
import numpy as np
import sub


def test_rates_within_15_percent():
    for kappa in (10, 100, 1000):
        lam = np.geomspace(1, kappa, 50)
        x0 = np.ones(50)
        for name, f, iters in (("gd", sub.gd, 40 * kappa), ("heavy_ball", sub.heavy_ball, int(60 * math.sqrt(kappa))), ("nesterov", sub.nesterov, int(60 * math.sqrt(kappa)))):
            e = f(lam, x0, iters)
            stop = int(np.argmax(e < 1e-200)) if np.any(e < 1e-200) else len(e)
            r = sub.measured_rate(e, stop // 2, stop)
            p = sub.proved_rate(name, kappa)
            assert abs(math.log(r) / math.log(p) - 1) < 0.15, (kappa, name, r, p)


def test_sgd_one_over_k():
    mse = sub.sgd_inverse_time(1.0, 1.0, 2.0, 10, 4000, 4000, np.random.default_rng(1))
    k = np.arange(1, 4001)
    slope = np.polyfit(np.log(k[400:]), np.log(mse[400:]), 1)[0]
    assert abs(slope + 1) < 0.15, slope


def test_bias_correction():
    a, b = sub.bias_correction(0.9, 0.999, 1)
    assert abs(a - 10) < 1e-9 and abs(b - 1000) < 1e-6
    rng = np.random.default_rng(2)
    G = 3.0 + rng.standard_normal((20000, 10))
    m = np.zeros(20000)
    for t in range(1, 11):
        m = 0.9 * m + 0.1 * G[:, t - 1]
        assert abs(m.mean() / 3.0 - sub.uncorrected_mean(0.9, t)) < 0.01
        assert abs(m.mean() * sub.bias_correction(0.9, 0.999, t)[0] - 3.0) < 0.03

import math
import numpy as np
import sub

TRUE = 0.5 * math.erfc(3 / math.sqrt(2))


def test_logpdf():
    assert abs(float(sub.normal_logpdf(0.0)) + 0.5 * math.log(2 * math.pi)) < 1e-12
    assert abs(float(sub.normal_logpdf(3.0, 1.0, 2.0)) - (-0.5 - math.log(2 * math.sqrt(2 * math.pi)))) < 1e-12


def test_rare_tail():
    rng = np.random.default_rng(9)
    f = lambda x: (x > 3).astype(float)
    naive = sub.is_estimate(f, sub.normal_logpdf, sub.normal_logpdf, rng.standard_normal(100000))
    xs = 3 + rng.standard_normal(100000)
    imp = sub.is_estimate(f, sub.normal_logpdf, lambda x: sub.normal_logpdf(x, 3.0), xs)
    assert abs(imp[0] - TRUE) < 4 * imp[1] and abs(naive[0] - TRUE) < 4 * naive[1]
    assert imp[1] < naive[1] / 10


def test_ess():
    assert abs(sub.ess(np.ones(50)) - 50) < 1e-12
    assert abs(sub.ess([1.0, 0.0, 0.0]) - 1) < 1e-12
    xs = np.random.default_rng(10).normal(0, 1.5, 20000)
    w = np.exp(sub.normal_logpdf(xs) - sub.normal_logpdf(xs, 0.0, 1.5))
    assert 0.5 * 20000 < sub.ess(w) < 20000

import math
import numpy as np
import sub


def test_noised_mixture():
    rng = np.random.default_rng(0)
    w, m, s = np.array([0.4, 0.6]), np.array([-2.0, 1.5]), np.array([0.4, 0.6])
    k = rng.choice(2, size=100000, p=w)
    x0 = m[k] + s[k] * rng.standard_normal(100000)
    xt = sub.noise(x0, 0.5, rng)
    w2, m2, s2 = sub.noised_params(w, m, s, 0.5)
    k2 = rng.choice(2, size=100000, p=w2)
    ref = m2[k2] + s2[k2] * rng.standard_normal(100000)
    q = np.linspace(0.05, 0.95, 19)
    assert np.max(np.abs(np.quantile(xt, q) - np.quantile(ref, q))) < 0.04


def test_forgetting_rate():
    vals = []
    for t in (2.0, 3.0, 4.0):
        a = math.exp(-t)
        vals.append(sub.kl_to_standard_normal(3.0 * a, 0.25 * a * a + 1 - a * a))
    assert abs(vals[1] / vals[0] - math.exp(-2)) < 0.02 and abs(vals[2] / vals[1] - math.exp(-2)) < 0.01

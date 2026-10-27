import numpy as np
import sub


def test_fair_die():
    m, v = sub.moments(np.arange(1, 7), np.full(6, 1 / 6))
    assert abs(m - 3.5) < 1e-12 and abs(v - 35 / 12) < 1e-12


def test_bernoulli():
    m, v = sub.moments(np.array([0, 1]), np.array([0.7, 0.3]))
    assert abs(m - 0.3) < 1e-12 and abs(v - 0.21) < 1e-12


def test_affine_rule_matches_direct_computation():
    vals = np.array([-2.0, 0.5, 3.0])
    p = np.array([0.2, 0.5, 0.3])
    m, v = sub.moments(vals, p)
    m2, v2 = sub.moments(-3 * vals + 7, p)
    am, av = sub.affine_moments(m, v, -3, 7)
    assert abs(am - m2) < 1e-12 and abs(av - v2) < 1e-12


def test_average_variance_by_simulation():
    rng = np.random.default_rng(0)
    means = rng.uniform(size=(20000, 10)).mean(axis=1)
    pred = sub.average_variance(1 / 12, 10)
    assert abs(means.var() - pred) / pred < 0.05

import numpy as np
import sub


def test_pareto_samples():
    x = sub.pareto(3.0, 400000, np.random.default_rng(70))
    assert x.min() >= 1 and abs(x.mean() - 1.5) < 0.01
    assert sub.pareto(1.5, (3, 4), np.random.default_rng(1)).shape == (3, 4)


def test_coverage_collapses_without_variance():
    rng = np.random.default_rng(71)
    exp_cov = sub.coverage(rng.exponential(size=(2000, 100)), 1.0)
    par = sub.pareto(1.5, (2000, 100), rng)
    par_cov = sub.coverage(par, 3.0)
    assert exp_cov > 0.92, exp_cov
    assert par_cov < 0.85, par_cov
    assert np.median(par.mean(axis=1)) < 3

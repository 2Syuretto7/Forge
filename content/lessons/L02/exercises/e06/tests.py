import math
import numpy as np
import sub


def _beta_cdf_grid(a, b, m=200001):
    t = np.linspace(0, 1, m)
    with np.errstate(divide="ignore"):
        logpdf = (a - 1) * np.log(t) + (b - 1) * np.log1p(-t) - (math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))
    pdf = np.exp(np.nan_to_num(logpdf, neginf=-np.inf))
    cdf = np.cumsum(pdf) * (t[1] - t[0])
    return t, cdf / cdf[-1]


def test_conjugate_update():
    assert sub.posterior_params(2, 3, 7, 10) == (9, 6)


def test_map_and_mean():
    assert abs(sub.map_estimate(1, 1, 3, 4) - 0.75) < 1e-12, "uniform prior: MAP equals MLE"
    assert abs(sub.map_estimate(2, 2, 3, 3) - 4 / 5) < 1e-12
    assert abs(sub.posterior_mean(1, 1, 0, 3) - 0.2) < 1e-12


def test_credible_interval_matches_exact_quantiles():
    t, cdf = _beta_cdf_grid(4, 2)
    lo_ref = t[np.searchsorted(cdf, 0.025)]
    hi_ref = t[np.searchsorted(cdf, 0.975)]
    lo, hi = sub.credible_interval(4, 2, 0.95, 200000, seed=1)
    assert abs(lo - lo_ref) < 0.01 and abs(hi - hi_ref) < 0.01, (lo, hi, lo_ref, hi_ref)


def test_more_data_narrows_the_interval():
    w_small = np.subtract(*sub.credible_interval(*sub.posterior_params(1, 1, 3, 4))[::-1])
    w_big = np.subtract(*sub.credible_interval(*sub.posterior_params(1, 1, 75, 100))[::-1])
    assert w_big < w_small / 3

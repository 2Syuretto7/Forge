import numpy as np
import sub

U = np.linspace(0.05, 0.95, 37)
PAIRS = [
    (lambda u: sub.laplace_quantile(u, 0.7), lambda x: sub.laplace_pdf(x, 0.7)),
    (sub.cauchy_quantile, sub.cauchy_pdf),
    (lambda u: sub.pareto_quantile(u, 3.0, 2.0), lambda x: sub.pareto_pdf(x, 3.0, 2.0)),
]


def test_grad_quantile_slope():
    h = 1e-6
    for q, f in PAIRS:
        slope = (q(U + h) - q(U - h)) / (2 * h)
        assert np.allclose(slope, 1 / f(q(U)), rtol=1e-5), np.max(np.abs(slope * f(q(U)) - 1))


def test_samples_have_the_right_cdf():
    u = np.random.default_rng(7).random(200000)
    x = sub.laplace_quantile(u, 0.7)
    assert abs(np.mean(x <= 1.0) - (1 - 0.5 * np.exp(-1 / 0.7))) < 0.004
    assert abs(np.mean(x <= -0.5) - 0.5 * np.exp(-0.5 / 0.7)) < 0.004
    c = sub.cauchy_quantile(u)
    assert abs(np.mean(np.abs(c) <= 1) - 0.5) < 0.004


def test_pareto_mean_and_support():
    u = (np.arange(1_000_000) + 0.5) / 1_000_000
    x = sub.pareto_quantile(u, 3.0, 2.0)
    assert x.min() >= 2.0
    assert abs(x.mean() - 3.0) < 0.01
    assert float(sub.pareto_pdf(1.0, 3.0, 2.0)) == 0.0

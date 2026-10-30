import math
import numpy as np
import sub

CASES = [
    (lambda x: sub.uniform_pdf(x, -1, 3), lambda x: sub.uniform_cdf(x, -1, 3), np.linspace(-0.9, 2.9, 37), (-1, 3)),
    (lambda x: sub.exponential_pdf(x, 2.5), lambda x: sub.exponential_cdf(x, 2.5), np.linspace(0.01, 4, 40), (0, 30)),
    (lambda x: sub.normal_pdf(x, 1, 0.5), lambda x: sub.normal_cdf(x, 1, 0.5), np.linspace(-1, 3, 41), (-6, 8)),
]


def test_grad_cdf_is_pdf():
    h = 1e-5
    for pdf, cdf, xs, _ in CASES:
        num = (cdf(xs + h) - cdf(xs - h)) / (2 * h)
        assert np.allclose(num, pdf(xs), rtol=1e-5, atol=1e-8), np.max(np.abs(num - pdf(xs)))


def test_densities_integrate_to_one():
    for pdf, cdf, _, (lo, hi) in CASES:
        x = np.linspace(lo, hi, 400001)
        y = pdf(x)
        area = float(np.sum((y[1:] + y[:-1]) / 2) * (x[1] - x[0]))
        assert abs(area - 1) < 1e-3, area
        assert abs(float(cdf(hi)) - 1) < 1e-12 and abs(float(cdf(lo))) < 1e-12


def test_values_and_shapes():
    assert abs(float(sub.normal_cdf(1.96, 0, 1)) - 0.9750021048517795) < 1e-12
    assert abs(float(sub.exponential_cdf(1, 2)) - (1 - math.exp(-2))) < 1e-15
    assert float(sub.exponential_pdf(-800, 2)) == 0.0 and float(sub.exponential_cdf(-1, 2)) == 0.0
    assert sub.normal_pdf(np.zeros((2, 3)), 0, 1).shape == (2, 3)
    assert float(sub.normal_pdf(0, 0, 0.1)) > 1

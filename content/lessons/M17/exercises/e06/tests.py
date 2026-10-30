import math
import sub

gauss = lambda x: math.exp(-x * x / 2)  # noqa: E731
beta22 = lambda x: x * (1 - x)  # noqa: E731


def test_normalizers():
    assert abs(sub.normalizer(gauss, -10, 10) - math.sqrt(2 * math.pi)) < 1e-10
    assert abs(sub.beta_normalizer(2, 2) - 1 / 6) < 1e-15
    g = lambda x: x ** 1.5 * (1 - x) ** 2.5  # noqa: E731
    assert abs(sub.normalizer(g, 0, 1) - sub.beta_normalizer(2.5, 3.5)) < 1e-7


def test_probabilities():
    cdf = sub.make_cdf(beta22, 0, 1)
    assert abs(cdf(0.3) - cdf(0.2) - 0.112) < 1e-12
    pdf = sub.make_pdf(beta22, 0, 1)
    assert abs(pdf(0.5) - 1.5) < 1e-12


def test_grad_cdf_derivative_is_pdf():
    cdf, pdf = sub.make_cdf(gauss, -10, 10, 400), sub.make_pdf(gauss, -10, 10)
    h = 1e-4
    for x in (-1.5, 0.0, 0.7, 2.2):
        assert abs((cdf(x + h) - cdf(x - h)) / (2 * h) - pdf(x)) < 1e-6

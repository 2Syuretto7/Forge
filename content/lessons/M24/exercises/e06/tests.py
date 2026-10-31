import math
import numpy as np
import sub


def test_grad_mgf_gives_moments():
    cases = [
        (lambda t: sub.mgf_bernoulli(t, 0.3), 0.3, 0.3),
        (lambda t: sub.mgf_normal(t, 1.5, 2.0), 1.5, 1.5**2 + 4.0),
        (lambda t: sub.mgf_exponential(t, 2.0), 0.5, 0.5),
    ]
    for M, m1, m2 in cases:
        a, b = sub.moments_from_mgf(M)
        assert abs(a - m1) < 1e-6 and abs(b - m2) < 1e-5, (a, b, m1, m2)


def test_sum_is_binomial():
    M = sub.mgf_of_sum(lambda t: sub.mgf_bernoulli(t, 0.3), 12)
    for t in (-1.0, 0.4, 1.3):
        binom = sum(math.comb(12, k) * 0.3**k * 0.7 ** (12 - k) * math.exp(t * k) for k in range(13))
        assert abs(M(t) - binom) < 1e-9 * binom


def test_standardized_sum_approaches_normal():
    p, n = 0.3, 100000
    s = math.sqrt(n * p * (1 - p))
    M = sub.mgf_of_sum(lambda t: sub.mgf_bernoulli(t, p), n)
    for t in (0.5, 1.0, 2.0):
        log_m = math.log(M(t / s)) - t * n * p / s
        assert abs(log_m - t * t / 2) < 0.01 * max(1, t**3)

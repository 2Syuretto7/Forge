import math
import sub


def test_short_texts_agree():
    ps = [0.5, 0.25, 0.1]
    assert abs(sub.log_likelihood(ps) - sub.log_likelihood_naive(ps)) < 1e-12


def test_long_text():
    ps = [0.01] * 1000
    assert sub.likelihood_product(ps) == 0.0
    assert sub.log_likelihood_naive(ps) == -math.inf
    assert abs(sub.log_likelihood(ps) - 1000 * math.log(0.01)) < 1e-8


def test_underflow_length():
    n = sub.underflow_length(0.01)
    assert 160 <= n <= 165, n
    assert sub.underflow_length(0.5) == 1075

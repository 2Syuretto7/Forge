import math
import sub

p = lambda x: 6 * x * (1 - x)  # noqa: E731


def test_beta():
    assert abs(sub.prob_between(p, 0.2, 0.3) - 0.112) < 1e-12
    assert abs(sub.mean(p, 0, 1) - 0.5) < 1e-12
    assert abs(sub.variance(p, 0, 1) - 0.05) < 1e-12
    assert abs(sub.quantile(p, 0, 1, 0.5) - 0.5) < 1e-8


def test_exponential():
    e = lambda x: math.exp(-x)  # noqa: E731
    assert abs(sub.quantile(e, 0, 40, 0.5) - math.log(2)) < 1e-6
    assert abs(sub.mean(e, 0, 40) - 1) < 1e-8

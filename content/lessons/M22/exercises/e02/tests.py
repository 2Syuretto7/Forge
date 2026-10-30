import math
import sub


def test_values():
    assert sub.bernoulli_pmf(1, 0.3) == 0.3 and abs(sub.bernoulli_pmf(0, 0.3) - 0.7) < 1e-15
    assert sub.bernoulli_pmf(2, 0.3) == 0.0
    assert abs(sub.binomial_pmf(2, 3, 0.5) - 3 / 8) < 1e-15
    assert sub.binomial_pmf(4, 3, 0.5) == 0.0 and sub.binomial_pmf(-1, 3, 0.5) == 0.0
    assert abs(sub.poisson_pmf(0, 3) - math.exp(-3)) < 1e-15
    assert 0 < sub.poisson_pmf(150, 120) < 1


def test_sums_and_moments():
    for n, p in [(10, 0.3), (40, 0.9)]:
        probs = [sub.binomial_pmf(k, n, p) for k in range(n + 1)]
        mean = sum(k * q for k, q in enumerate(probs))
        var = sum(k * k * q for k, q in enumerate(probs)) - mean**2
        assert abs(sum(probs) - 1) < 1e-12 and abs(mean - n * p) < 1e-10 and abs(var - n * p * (1 - p)) < 1e-9
    probs = [sub.poisson_pmf(k, 4.5) for k in range(80)]
    mean = sum(k * q for k, q in enumerate(probs))
    var = sum(k * k * q for k, q in enumerate(probs)) - mean**2
    assert abs(sum(probs) - 1) < 1e-12 and abs(mean - 4.5) < 1e-10 and abs(var - 4.5) < 1e-9


def test_cdf():
    assert abs(sub.cdf_from_pmf(lambda j: sub.binomial_pmf(j, 3, 0.5), 1) - 0.5) < 1e-15
    assert abs(sub.cdf_from_pmf(lambda j: sub.poisson_pmf(j, 2.0), 60) - 1) < 1e-12


def test_poisson_limit():
    def gap(n):
        return max(abs(sub.binomial_pmf(k, n, 3 / n) - sub.poisson_pmf(k, 3)) for k in range(20))

    assert gap(1000) < 0.001
    assert gap(1000) < gap(100) / 5

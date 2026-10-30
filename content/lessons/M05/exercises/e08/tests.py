import math
import sub


def test_exponents():
    assert abs(sub.exponent_estimate(lambda n: 3 * n * n + n, 1000) - 2) < 0.01
    assert abs(sub.exponent_estimate(lambda n: n ** 3 / 6, 1000) - 3) < 1e-9


def test_classify():
    assert sub.classify(lambda n: 7) == "constant"
    assert sub.classify(lambda n: math.log2(n)) == "logarithmic"
    assert sub.classify(lambda n: 5 * n + 3) == "linear"
    assert sub.classify(lambda n: n * math.log2(n)) == "n log n"
    assert sub.classify(lambda n: n * (n - 1) / 2) == "quadratic"
    assert sub.classify(lambda n: n ** 3) == "cubic"
    assert sub.classify(lambda n: 2.0 ** min(n, 1000), n=64) == "exponential"

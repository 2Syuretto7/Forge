import math
import sub


def test_grad_log_mgf():
    h = 1e-6
    for t in (0.0, 0.5, 2.0):
        for p in (0.1, 0.5, 0.8):
            num = (sub.log_mgf(t + h, p) - sub.log_mgf(t - h, p)) / (2 * h)
            assert abs(num - sub.d_log_mgf(t, p)) < 1e-8


def test_exponent_is_kl():
    for a, p in ((0.6, 0.5), (0.3, 0.1), (0.95, 0.9)):
        assert abs(sub.chernoff_exponent(a, p) - sub.kl_bernoulli(a, p)) < 1e-9


def test_between_exact_and_hoeffding():
    n, p, a = 500, 0.3, 0.36
    exact = sum(math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log(1 - p)) for k in range(math.ceil(n * a - 1e-9), n + 1))
    c = sub.chernoff_bound(n, a, p)
    assert exact <= c <= math.exp(-2 * n * (a - p) ** 2)

import math
import numpy as np
import sub


def test_grad_log_mgf_chi2():
    h = 1e-6
    for t in (-0.5, 0.0, 0.2, 0.4):
        for k in (1, 7, 50):
            num = (sub.log_mgf_chi2(t + h, k) - sub.log_mgf_chi2(t - h, k)) / (2 * h)
            assert abs(num - sub.d_log_mgf_chi2(t, k)) < 1e-5 * max(1, abs(num))


def test_chain_of_bounds():
    rng = np.random.default_rng(0)
    for k, eps in ((20, 0.5), (100, 0.3), (400, 0.15)):
        emp = sub.empirical_upper(k, eps, 200000, rng)
        assert emp <= sub.chernoff_upper(k, eps) <= sub.simple_upper(k, eps)


def test_union_bound():
    k = math.ceil(4 * math.log(200) / (0.3**2 / 2 - 0.3**3 / 3))
    assert sub.union_failure(200, k, 0.3) < 1
    assert sub.union_failure(200, k // 2, 0.3) > 1

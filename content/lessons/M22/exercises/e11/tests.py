import math
import numpy as np
import sub

erf = np.vectorize(math.erf)
N = 10**6


def phi(x):
    return 0.5 * (1 + erf(np.asarray(x) / math.sqrt(2)))


def poisson_cdf(lam, K):
    return np.cumsum([math.exp(k * math.log(lam) - lam - math.lgamma(k + 1)) for k in range(K)])


def test_threshold():
    assert abs(sub.dkw_threshold(N, 0.05) - 1.3581 / 1000) < 1e-6


def test_gaussian():
    z = np.random.default_rng(12).standard_normal(N)
    assert sub.ks_distance(z, phi) < sub.dkw_threshold(N, 0.01)
    assert sub.ks_distance(z + 0.02, phi) > 3 * sub.dkw_threshold(N, 0.01)


def test_poisson():
    k = np.random.default_rng(13).poisson(3.0, N)
    assert sub.discrete_distance(k, poisson_cdf(3.0, 30)) < sub.dkw_threshold(N, 0.01)
    assert sub.discrete_distance(k, poisson_cdf(3.1, 30)) > 5 * sub.dkw_threshold(N, 0.01)


def test_small_case():
    assert abs(sub.ks_distance(np.array([0.5]), lambda x: x) - 0.5) < 1e-12
    assert abs(sub.discrete_distance(np.array([0, 0, 1, 2]), [0.5, 0.75, 1.0])) < 1e-12

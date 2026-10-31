import math
import numpy as np
import sub

N = 10**6
erf = np.vectorize(math.erf)
LIMIT = math.sqrt(math.log(2 / 0.001) / (2 * N))


def ks(x, cdf):
    x = np.sort(np.asarray(x, dtype=float))
    F = cdf(x)
    i = np.arange(1, len(x) + 1)
    return float(max(np.max(i / len(x) - F), np.max(F - (i - 1) / len(x))))


def discrete(x, cdf_values):
    counts = np.bincount(x, minlength=len(cdf_values))[: len(cdf_values)]
    return float(np.max(np.abs(np.cumsum(counts) / len(x) - np.asarray(cdf_values))))


def pmf_table(f, K):
    return np.cumsum([f(k) for k in range(K)])


class OnlyUniforms:
    def __init__(self, seed):
        self.g = np.random.default_rng(seed)

    def random(self, size=None):
        return self.g.random(size)


def test_discrete_samplers():
    cases = [
        (lambda r: sub.bernoulli(0.3, N, r), pmf_table(lambda k: [0.7, 0.3][k], 2)),
        (lambda r: sub.binomial(20, 0.35, N, r), pmf_table(lambda k: math.comb(20, k) * 0.35**k * 0.65 ** (20 - k), 21)),
        (lambda r: sub.geometric(0.2, N, r), np.concatenate([[0.0], 1 - 0.8 ** np.arange(1, 80)])),
        (lambda r: sub.poisson(6.5, N, r), pmf_table(lambda k: math.exp(k * math.log(6.5) - 6.5 - math.lgamma(k + 1)), 40)),
    ]
    for i, (draw, cdf) in enumerate(cases):
        x = draw(OnlyUniforms(100 + i))
        assert x.shape == (N,) and np.issubdtype(x.dtype, np.integer), i
        assert discrete(x, cdf) < LIMIT, (i, discrete(x, cdf), LIMIT)
    assert sub.geometric(0.2, N, OnlyUniforms(1)).min() == 1


def test_continuous_samplers():
    cases = [
        (lambda r: sub.uniform(-2, 5, N, r), lambda x: np.clip((x + 2) / 7, 0, 1)),
        (lambda r: sub.exponential(1.5, N, r), lambda x: -np.expm1(-1.5 * x)),
        (lambda r: sub.laplace(0.8, N, r), lambda x: np.where(x < 0, 0.5 * np.exp(np.minimum(x, 0) / 0.8), 1 - 0.5 * np.exp(-np.maximum(x, 0) / 0.8))),
        (lambda r: sub.gaussian(1.0, 2.0, N, r), lambda x: 0.5 * (1 + erf((x - 1.0) / (2.0 * math.sqrt(2))))),
    ]
    for i, (draw, cdf) in enumerate(cases):
        x = draw(OnlyUniforms(200 + i))
        assert x.shape == (N,), i
        assert ks(x, cdf) < LIMIT, (i, ks(x, cdf), LIMIT)
    assert sub.gaussian(0.0, 1.0, 7, OnlyUniforms(3)).shape == (7,)


def test_init_scale():
    assert sub.leaky_second_moment(0.0) == 0.5 and sub.leaky_second_moment(1.0) == 1.0
    assert abs(sub.init_std(512, 0.0) - 0.0625) < 1e-12
    assert abs(sub.init_std(512, 1.0) - 1 / math.sqrt(512)) < 1e-12
    for a in (0.0, 0.2):
        m = sub.depth_check(40, 128, a)
        assert len(m) == 40 and 0.9 < m[-1] ** (1 / 40) < 1.1, (a, m[-1])
    assert sub.depth_check(40, 128, 0.2, 0.8)[-1] < 1e-5
    assert sub.depth_check(40, 128, 0.2, 1.25)[-1] > 1e5

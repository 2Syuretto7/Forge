import numpy as np
import sub


def test_merge_matches_numpy():
    x = np.random.default_rng(1).normal(3.0, 2.0, size=1003)
    acc = (0, 0.0, 0.0)
    for part in np.split(x, [1, 10, 400, 999]):
        acc = sub.merge(acc, sub.chunk_stats(part))
    assert acc[0] == 1003
    assert abs(acc[1] - x.mean()) < 1e-12 and abs(acc[2] / 1002 - x.var(ddof=1)) < 1e-10
    assert sub.merge((0, 0.0, 0.0), (5, 2.0, 3.0)) == (5, 2.0, 3.0)


def test_ten_million_exponentials():
    rng = np.random.default_rng(10)
    m, v = sub.streaming_moments(lambda k: -np.log1p(-rng.random(k)), 10**7)
    assert abs(m - 1) < 4 * sub.mean_se(1.0, 10**7), m
    assert abs(v - 1) < 4 * sub.var_se(1.0, 9.0, 10**7), v


def test_ten_million_uniforms():
    rng = np.random.default_rng(11)
    m, v = sub.streaming_moments(lambda k: rng.random(k), 10**7, chunk=2_500_000)
    assert abs(m - 0.5) < 4 * sub.mean_se(1 / 12, 10**7)
    assert abs(v - 1 / 12) < 4 * sub.var_se(1 / 12, 1 / 80, 10**7)
    assert sub.mean_se(1 / 12, 10**7) < 1e-4

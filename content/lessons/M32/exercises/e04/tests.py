import math
import numpy as np
import sub


def test_gap():
    for n in (5, 20, 50):
        assert abs(sub.spectral_gap(sub.lazy_cycle(n)) - 0.5 * (1 - math.cos(2 * math.pi / n))) < 1e-10
    assert sub.tv([1, 0], [0, 1]) == 1.0 and sub.tv([0.5, 0.5], [0.5, 0.5]) == 0.0


def test_mixing_grows_like_n_squared():
    t20 = sub.mixing_time(sub.lazy_cycle(20))
    t40 = sub.mixing_time(sub.lazy_cycle(40))
    assert 3.5 < t40 / t20 < 4.5, (t20, t40)
    gap = sub.spectral_gap(sub.lazy_cycle(40))
    assert t40 <= math.log(1 / (0.25 / 40)) / gap


def test_rate_is_the_second_eigenvalue():
    P = sub.lazy_cycle(20)
    u = np.ones(20) / 20
    d = np.zeros(20)
    d[0] = 1
    dist = []
    for _ in range(400):
        d = d @ P
        dist.append(sub.tv(d, u))
    assert abs(dist[-1] / dist[-2] - (1 - sub.spectral_gap(P))) < 1e-3

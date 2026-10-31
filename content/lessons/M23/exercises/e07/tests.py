import numpy as np
import sub


def test_fuse():
    m, v = sub.fuse(10.0, 4.0, 12.0, 1.0)
    assert abs(m - 11.6) < 1e-12 and abs(v - 0.8) < 1e-12
    K = sub.gain(4.0, 1.0)
    assert abs(K - 0.8) < 1e-12 and abs(10 + K * 2 - m) < 1e-12


def test_many_equal_measurements_average():
    m, v = sub.fuse_many([1.0, 2.0, 6.0], [3.0, 3.0, 3.0])
    assert abs(m - 3.0) < 1e-12 and abs(v - 1.0) < 1e-12


def test_fusion_is_gaussian_conditioning():
    # x ~ N(m1, v1), y = x + noise with variance v2; conditioning x on y = m2 fuses the two.
    m1, v1, v2, y = 1.0, 2.0, 0.5, 3.0
    C = np.array([[v1, v1], [v1, v1 + v2]])
    cond_mean = m1 + C[0, 1] / C[1, 1] * (y - m1)
    cond_var = C[0, 0] - C[0, 1] ** 2 / C[1, 1]
    m, v = sub.fuse(m1, v1, y, v2)
    assert abs(m - cond_mean) < 1e-12 and abs(v - cond_var) < 1e-12


def test_order_does_not_matter():
    rng = np.random.default_rng(11)
    ms, vs = rng.normal(size=6), rng.uniform(0.5, 3, size=6)
    a = sub.fuse_many(ms, vs)
    b = sub.fuse_many(ms[::-1], vs[::-1])
    assert abs(a[0] - b[0]) < 1e-12 and abs(a[1] - b[1]) < 1e-12

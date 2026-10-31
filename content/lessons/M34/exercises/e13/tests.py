import numpy as np
import sub


def test_grad_softmax():
    z = np.array([0.3, -1.2, 2.0, 0.5])
    J = sub.softmax_jacobian(z)
    h = 1e-6
    for j in range(4):
        e = np.zeros(4)
        e[j] = h
        num = (sub.softmax(z + e) - sub.softmax(z - e)) / (2 * h)
        assert np.max(np.abs(num - J[:, j])) < 1e-8


def test_saturation():
    rng = np.random.default_rng(0)
    s64 = sub.attention_stats(64, 64, True, 200, rng)
    s1024 = sub.attention_stats(1024, 64, True, 200, rng)
    u1024 = sub.attention_stats(1024, 64, False, 200, rng)
    assert abs(s64[0] - s1024[0]) < 0.05 and abs(s64[1] - s1024[1]) < 0.05
    assert u1024[0] > 0.9 and u1024[1] < 0.1 * s1024[1], (s1024, u1024)
    assert abs(sub.softmax(np.array([1000.0, 0.0])).sum() - 1) < 1e-12

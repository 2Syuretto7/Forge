import numpy as np
import sub

V = 50000


def test_log_softmax():
    z = np.random.default_rng(1).normal(size=V)
    ls = sub.log_softmax(z)
    assert abs(np.exp(ls).sum() - 1) < 1e-10
    assert abs(sub.cross_entropy(np.zeros(V), 123) - np.log(V)) < 1e-10


def test_uniform_and_random_init():
    assert abs(sub.uniform_loss(V) - 10.819778284410283) < 1e-12
    small = sub.random_init_loss(V, 0.02)
    assert abs(small - np.log(V)) < 0.05
    big = sub.random_init_loss(V, 5.0)
    assert big > np.log(V) + 3, "large random logits make the first loss much worse than uniform"


def test_huge_logits():
    z = np.zeros(10)
    z[3] = 1e4
    assert sub.cross_entropy(z, 3) < 1e-12
    assert abs(sub.cross_entropy(z, 0) - 1e4) < 1e-6

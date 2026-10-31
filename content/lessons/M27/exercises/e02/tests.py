import numpy as np
import sub

rng = np.random.default_rng(2)


def test_gibbs_inequality():
    for _ in range(200):
        p, q = rng.dirichlet(np.ones(5)), rng.dirichlet(np.ones(5))
        assert sub.kl(p, q) >= -1e-15
    p = rng.dirichlet(np.ones(5))
    assert abs(sub.kl(p, p)) < 1e-15


def test_decomposition():
    p, q = rng.dirichlet(np.ones(4)), rng.dirichlet(np.ones(4))
    h = -np.sum(p * np.log(p))
    assert abs(sub.cross_entropy(p, q) - (h + sub.kl(p, q))) < 1e-12


def test_asymmetry_example():
    p, q = np.array([0.5, 0.5]), np.array([0.9, 0.1])
    assert abs(sub.kl(p, q) - 0.5108256237659907) < 1e-12
    assert abs(sub.kl(q, p) - 0.3680642071684971) < 1e-12


def test_zero_support():
    assert sub.kl(np.array([0.5, 0.5]), np.array([1.0, 0.0])) == float("inf")
    assert np.isfinite(sub.kl(np.array([1.0, 0.0]), np.array([0.5, 0.5])))
    assert sub.cross_entropy(np.array([0.0, 1.0]), np.array([0.3, 0.7])) == -np.log(0.7)

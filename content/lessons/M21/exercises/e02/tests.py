import numpy as np
import sub


def test_posterior_normalizes():
    p = sub.posterior(np.array([0.5, 0.3, 0.2]), np.array([0.1, 0.4, 0.4]))
    assert abs(p.sum() - 1) < 1e-12 and np.allclose(p, np.array([0.05, 0.12, 0.08]) / 0.25)


def test_puzzle():
    assert abs(sub.positive_test_posterior(0.001, 0.99, 0.01) - 0.00099 / 0.01098) < 1e-12


def test_two_positive_tests():
    p = sub.sequential(np.array([0.001, 0.999]), np.array([[0.99, 0.01], [0.99, 0.01]]))
    assert abs(p[0] - 9801 / (9801 + 999)) < 1e-12


def test_order_does_not_matter():
    rng = np.random.default_rng(3)
    L = rng.uniform(0.1, 1, size=(5, 4))
    prior = np.full(4, 0.25)
    assert np.allclose(sub.sequential(prior, L), sub.sequential(prior, L[::-1]))
    assert np.allclose(sub.sequential(prior, L), sub.posterior(prior, L.prod(axis=0)))

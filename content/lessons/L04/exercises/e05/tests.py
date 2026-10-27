import numpy as np
import sub

rng = np.random.default_rng(5)
K = 5
data = rng.choice(K, size=400, p=[0.1, 0.3, 0.05, 0.4, 0.15])


def test_avg_nll_is_cross_entropy():
    z = rng.normal(size=K)
    q = np.exp(z) / np.exp(z).sum()
    ph = sub.empirical(data, K)
    assert abs(sub.avg_nll(z, data) - (-np.sum(ph * np.log(q)))) < 1e-12


def test_grad_matches_finite_differences():
    z = rng.normal(size=K)
    g = sub.grad_avg_nll(z, data, K)
    num = np.zeros(K)
    for j in range(K):
        e = np.zeros(K)
        e[j] = 1e-6
        num[j] = (sub.avg_nll(z + e, data) - sub.avg_nll(z - e, data)) / 2e-6
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_fit_recovers_empirical_distribution():
    q = sub.fit(data, K, steps=3000, lr=1.0)
    assert np.allclose(q, sub.empirical(data, K), atol=1e-4)

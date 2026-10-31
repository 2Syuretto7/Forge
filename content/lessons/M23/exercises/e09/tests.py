import numpy as np
import sub

rng = np.random.default_rng(13)
X = rng.normal(size=(300, 3)) @ rng.normal(size=(3, 3)) + 1.0


def test_grad_mu():
    S = np.cov(X, rowvar=False) + 0.3 * np.eye(3)
    mu = np.array([0.2, -0.5, 1.5])
    g = sub.grad_mu(X, mu, S)
    h = 1e-6
    for k in range(3):
        e = np.zeros(3)
        e[k] = h
        num = (sub.nll(X, mu + e, S) - sub.nll(X, mu - e, S)) / (2 * h)
        assert abs(num - g[k]) < 1e-6


def test_mle_is_a_minimum():
    m, S = sub.mle(X)
    assert np.allclose(S, np.cov(X, rowvar=False, bias=True))
    best = sub.nll(X, m, S)
    assert np.allclose(sub.grad_mu(X, m, S), 0, atol=1e-12)
    for _ in range(20):
        d = rng.normal(size=3) * 0.05
        B = rng.normal(size=(3, 3)) * 0.05
        assert sub.nll(X, m + d, S) > best
        assert sub.nll(X, m, S + B @ B.T) > best
        assert sub.nll(X, m, S * (1 + rng.choice([-0.05, 0.05]))) > best

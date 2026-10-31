import numpy as np
import sub

W = np.array([0.3, 0.3, 0.4])
M = np.array([[-2.0, 0.0], [2.0, 1.0], [0.0, -2.0]])
S = 0.35


def test_grad_mixture2d_score():
    X = np.array([[0.1, -0.4], [-2.2, 0.3], [5.0, 5.0], [1.0, 1.0]])
    G = sub.mixture2d_score(X, W, M, S)
    h = 1e-6
    for j in range(2):
        e = np.zeros(2)
        e[j] = h
        num = (sub.mixture2d_logpdf(X + e, W, M, S) - sub.mixture2d_logpdf(X - e, W, M, S)) / (2 * h)
        assert np.max(np.abs(num - G[:, j]) / (1 + np.abs(num))) < 1e-5


def test_generates_target():
    rng = np.random.default_rng(0)
    k = rng.choice(3, size=2000, p=W)
    data = M[k] + S * rng.standard_normal((2000, 2))
    gen = sub.reverse_sample_2d(lambda x, t: sub.noised_score(x, t, W, M, S), 1000, 5.0, 100, rng)
    assert sub.sliced_w1(gen, data, rng) < 0.08
    assert sub.sliced_w1(rng.standard_normal((1000, 2)), data, rng) > 0.5
